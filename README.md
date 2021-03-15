# Frisenbrief-Bot

[![Lint Code Base](https://github.com/AV-Frisia/frisenbrief-bot/actions/workflows/linter.yml/badge.svg)](https://github.com/AV-Frisia/frisenbrief-bot/actions/workflows/linter.yml)

Konvertiert Mailanhänge nach LaTeX

## Nutzung

```console
usage: FrisenbriefBot.py [-h] [--host HOST] [--email EMAIL] [--passwort PASSWORT] [--datum TT-MMM-JJJJ] [--version]

E-Mail Anhänge in LaTeX konvertieren

optional arguments:
  -h, --help           show this help message and exit
  --host HOST          E-Mail Server (IMAP) das gescannt wird
  --email EMAIL        E-Mail Nutzer (Adresse)
  --passwort PASSWORT  Password des kontos
  --datum TT-MMM-JJJJ  Datum, ab dem E-Mails gesucht werden. (Normalerweise Semesterbeginn)
  --version            show program's version number and exit

```

Nach der Installation aller Abhängigkeiten kann das Programm ausgeführt werden.

Wenn keine Argumente gegeben sind, wird Interaktiv angefragt.

## To-Do

Allgemeine Umstrukturierung

- [ ] `requirements.txt` generieren
- [ ] Rechtschreibprüfung
- [ ] Spaghetticode eliminieren
  - [ ] `tempfile` Modul benutzen anstelle von festkodiertem `/tmp/`
  - [ ] Windows Kompatabilität
- [ ] E-Mail Metadaten als Kommentar einbringen (Sender, Betreff, etc.)
