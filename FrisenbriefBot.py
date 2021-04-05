#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging
import email
from email.header import decode_header
import os
from imapclient import IMAPClient
import glob
import pypandoc
import textract
from pylatexenc.latexencode import unicode_to_latex
import argparse
from getpass import getpass

from pathvalidate import sanitize_filename

import uuid
#import hashlib

logging.basicConfig(filename='bot.log',level=logging.DEBUG)

def fetch_messages(host, email_addr, password, since):
    with IMAPClient(host) as server:
        server.login(email_addr, password)
        server.select_folder('INBOX', readonly=True)
        
        print('Erfolgreich eingeloggt zu konto', email_addr)
        
        messages = server.search('TO frisenbrief@avfrisia.de SINCE ' + since)
        
        emails = []
        
        for uid, message_data in server.fetch(messages, 'RFC822').items():
            email_message = email.message_from_bytes(message_data[b'RFC822'])
            #print(uid, email_message.get('From'), email_message.get('Subject'))
            emails.append(email_message)
            
        print(len(emails), 'mails gefunden')
        return emails
            
def get_attachments(emails, download_dir='/tmp/frisenbriefbot'):    
    for email in emails:
        for part in email.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            
            filename = part.get_filename()
            
            #filename = sanitize_filename(filename)

            try:
                if decode_header(filename)[0][1] is not None:
                    filename = decode_header(filename)[0][0].decode(decode_header(filename)[0][1])
            except TypeError:
                print("Error decoding. Using UUID")
                filename = str(uuid.uuid4())
            
            att_path = os.path.join(download_dir, filename)
            
            if not os.path.exists(download_dir):
                os.makedirs(download_dir)

            if not os.path.isfile(att_path):
                fp = open(att_path, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
                #print('Downloaded file:', filename)
                
def convert(from_dir, to_dir):
    types = ('*.doc', '*.docx', '*.odt', '*.pdf')
    files_grabbed = []
    
    for files in types:
        files_grabbed.extend(glob.glob(os.path.join(from_dir, files)))
    
    print("Found", len(files_grabbed), "files")
    
    if not os.path.exists(to_dir):
        os.makedirs(to_dir)
    
    for filename in files_grabbed:
        names = os.path.splitext(os.path.basename(filename))
        file_title = names[0]
        file_extension = names[1]
        
        out_file = os.path.join(to_dir, file_title + '.tex')

        file_format = file_extension[1:]

        file_contents = str()

        # use pypandoc for all supported types
        if file_format in pypandoc.get_pandoc_formats()[0]:
            file_contents = "% Konvertiert von " + file_format + "\n"
            file_contents += pypandoc.convert_file(filename, "latex")
        else:
            # mainly PDFs
            text = textract.process(filename)
            file_contents = "% ACHTUNG: Formatierung fehlt.\n"
            file_contents += unicode_to_latex(text.decode('utf-8'))

        # Write metadata into file
        fp = open(out_file, 'w')
        fp.write(file_contents)
        fp.close()

        print('[', file_format, ']', 'Konvertiert zu', out_file)


def main():
    # set up command line arguments
    parser = argparse.ArgumentParser(description='E-Mail Anhänge in LaTeX konvertieren')
    parser.add_argument('--host', help='E-Mail Server (IMAP) das gescannt wird', type=str)
    parser.add_argument('--email', help='E-Mail Nutzer (Adresse)', type=str)
    parser.add_argument('--passwort', help='Password des kontos', type=str)
    parser.add_argument('--datum', help='Datum, ab dem E-Mails gesucht werden. (Normalerweise Semesterbeginn)', type=str, metavar='TT-MMM-JJJJ')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    args = parser.parse_args()
    
    # prompt for missing variables interactively
    if args.host is None:
        args.host = input("IMAP Server: ") 
    if args.email is None:
        args.email = input("E-Mail: ") 
    if args.passwort is None:
        args.passwort = getpass()
    if args.datum is None:
        args.datum = input("Ab Datum (TT-MMM-JJJ): ")

    
    try:
        # connect to the mail server
        msgs = fetch_messages(args.host, args.email, args.passwort, args.datum);
    except:
        print("Fehler beim einloggen.")
        sys.exit(1)
            
    get_attachments(msgs, "/tmp/frisenbriefbot")
    convert("/tmp/frisenbriefbot", "/tmp/frisenbriefbot/converted/")
  
if __name__== "__main__":
  main()
