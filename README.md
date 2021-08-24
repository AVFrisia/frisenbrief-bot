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

Nach der Installation aller Abhängigkeiten in `requirements.txt` kann das Programm ausgeführt werden.

Wenn keine Argumente gegeben sind, wird Interaktiv angefragt.

## Ausgabe

LaTeX Dateien werden im `output` Ordner nach Absender und Betreff sortiert. Für jede Mail (falls Lesen erfolgreich) der Ordner `original` erstellt, mit allen Originalanhängen.

## Performance

* Disk I/O: der großteil der Daten befinden sich im Hauptspeicher vor und während der Konvertierung. Auf *nix ist es vorteilhaft, `/tmp` als tmpfs gemountet zu haben
* Parallelität:
  * Jede E-Mail wird in seperatem Prozess behandelt
  * Skaliert mit Anzahl Kernen
* Bilder werden übersprungen und direkt in der `original`-Ordner gespeichert

## Installation

Der Bot hat Abhängigkeiten für `antiword`, `textract`, und `pandoc`. Alle weiteren Python-Abhängigkeiten können über Pip oder dem `.venv` installiert werden.
