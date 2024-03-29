#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import pypandoc
import textract
from pylatexenc.latexencode import unicode_to_latex
import argparse
from getpass import getpass
from pathvalidate import sanitize_filename
import datetime
from imbox import Imbox
import tempfile
from multiprocessing import Pool
from datetime import datetime
import subprocess
import chardet
import signal
import sys

LOGLEVEL = os.environ.get("LOGLEVEL", "WARNING").upper()
logging.basicConfig(level=LOGLEVEL)

OUTPUT_DIR = "output"


def fetch_messages(host, email_addr, password, since):
    """Filter Email messages and process them concurrently"""
    with Imbox(
        host,
        username=email_addr,
        password=password,
        ssl=True,
        ssl_context=None,
        starttls=False,
    ) as imbox:
        status, folders = imbox.folders()
        print(f"{status}, {len(folders)} folders")

        messages = imbox.messages(sent_to="frisenbrief@avfrisia.de", date__gt=since)

        print(f"Got {len(messages)} messages")

        # The virgin iterating over individual emails
        # The chad taking advantage of all cores
        with Pool() as pool:
            converted = pool.starmap(process_email, messages)

            # Flatten all files by one level
            paths = [path for sublist in converted for path in sublist]

            finished = pool.map(touchup, filter(None, paths))

        for file in finished:
            print(file)


def process_email(uid, message):
    """Save attachments from an email to disk"""

    # Return an array of finished tex files
    processed_files = []

    # First, grab metadata
    if not hasattr(message, "subject"):
        logging.warning(f"Message with UID {uid} has no subject")
        message.subject = "[No Subject]"

    if message.sent_from[0]["name"]:
        sender = message.sent_from[0]["name"]
    else:
        sender = message.sent_from[0]["email"]

    # Sanitize metadata
    message.subject = sanitize_filename(message.subject)
    sender = sanitize_filename(sender)

    # Create folder to dump files in
    folder = os.path.join(OUTPUT_DIR, sender, message.subject)
    os.makedirs(folder, exist_ok=True)

    # Save, and if possible convert, each attachment
    for idx, attachment in enumerate(message.attachments):

        filename = sanitize_filename(attachment.get("filename"))

        # First, write our original file
        try:
            original_files_folder = os.path.join(folder, "original")
            os.makedirs(original_files_folder, exist_ok=True)
            original_file_path = os.path.join(original_files_folder, filename)
            original_file = open(original_file_path, "wb")
            original_file.write(attachment.get("content").getbuffer())
            original_file.close()
        except Exception as e:
            logging.exception(f"Could not save original attachment {filename}")

        # Infer file format from extension
        names = os.path.splitext(os.path.basename(filename))
        file_title = names[0]
        file_extension = names[1]
        file_format = file_extension[1:]

        # Convert the file
        converted = ""
        try:
            converted = convert(file_format, attachment.get("content").read())
        except Exception as e:
            logging.exception("Could not convert attachment")

        # If the file is successfully converted, write it to disk
        if converted:
            output_path = os.path.join(folder, file_title + ".tex")
            output_file = open(output_path, "w")

            # Add metadata to make it easier for the editor
            metadata_string = "% Von: {author}\r\n% Betreff: {subject}\r\n".format(
                author=sender, subject=message.subject
            )

            # Dump our converted file
            output_file.write(metadata_string)
            output_file.write(converted)
            output_file.close()

            processed_files.append(output_path)

    return processed_files


def convert(file_format, file_content):
    """Convert a string to a LaTeX string"""

    # File Format is critical for conversion
    if not file_format:
        return

    latex = ""

    # use pypandoc for all supported types
    if file_format in pypandoc.get_pandoc_formats()[0]:
        latex += pypandoc.convert_text(file_content, format=file_format, to="latex")
    elif file_format.lower() in ["txt"]:
        # Detect encoding (because fucking Notepad.exe doesn't do UTF-8 until Build 1903)
        en = chardet.detect(file_content)["encoding"]
        latex += unicode_to_latex(
            file_content.decode(encoding=en),
            unknown_char_policy="ignore",
            unknown_char_warning=False,
        )
    else:
        logging.warning(f"Falling back to textract for format {file_format}")

        # Textract wants a "regular" file
        tmp = tempfile.NamedTemporaryFile(suffix="." + file_format)
        tmp.write(file_content)

        # mainly PDFs or older .doc's
        text = textract.process(tmp.name, language='deu')
        latex = "% Achtung: Formatierung war nicht möglich.\r\n"
        latex += unicode_to_latex(
            text.decode(), unknown_char_policy="ignore", unknown_char_warning=False
        )

    return latex


def touchup(file: str):
    """Runs final touches (such as formatting) on a LaTeX file"""
    subprocess.run(["latexindent", file, "-s", "-m", "-o", file], check=True)
    return file


def cancelhandler(signum, frame):
    logging.critical(f"Files in {OUTPUT_DIR} may be incomplete")
    sys.exit()


def main():
    # Ensure we write to our own empty directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    if os.listdir(OUTPUT_DIR):
        sys.exit("Fehler: Ausgabeordner nicht leer")
    signal.signal(signal.SIGINT, cancelhandler)

    # set up command line arguments
    parser = argparse.ArgumentParser(description="E-Mail Anhänge in LaTeX konvertieren")
    parser.add_argument(
        "--host", help="E-Mail Server (IMAP) das gescannt wird", type=str
    )
    parser.add_argument("--email", help="E-Mail Nutzer (Adresse)", type=str)
    parser.add_argument("--passwort", help="Password des kontos", type=str)
    parser.add_argument(
        "--datum",
        help="Datum, ab dem E-Mails gesucht werden. (Normalerweise Semesterbeginn)",
        type=str,
        metavar="TT-MM-JJJJ",
    )
    parser.add_argument("--version", action="version", version="%(prog)s 1.0")
    args = parser.parse_args()

    # prompt for missing variables interactively
    if args.host is None:
        args.host = input("IMAP Server: ")
    if args.email is None:
        args.email = input("E-Mail: ")
    if args.passwort is None:
        args.passwort = getpass()
    if args.datum is None:
        args.datum = input("Ab Datum (TT-MM-JJJJ): ")

    date = datetime.strptime(args.datum, "%d-%m-%Y").date()

    fetch_messages(args.host, args.email, args.passwort, date)


if __name__ == "__main__":
    main()
