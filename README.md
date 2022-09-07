# Frisenbrief-Bot

[![Lint Code Base](https://github.com/AV-Frisia/frisenbrief-bot/actions/workflows/linter.yml/badge.svg)](https://github.com/AV-Frisia/frisenbrief-bot/actions/workflows/linter.yml)

Konvertiert Mailanhänge nach LaTeX

## Nutzung

```console
[johannes@kirby frisenbrief-bot]$ ./FrisenbriefBot.py -h
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

Wenn keine Argumente gegeben sind, wird Interaktiv angefragt.

## Ausgabe

LaTeX Dateien werden im `output` Ordner nach Absender und Betreff sortiert. Für jede Mail (falls Lesen erfolgreich) der Ordner `original` erstellt, mit allen Originalanhängen.

Konvertierte LaTeX-Dateien werden automatisch auf Sonderzeichen und ordentliche Zeilenlänge formatiert.

### Vorbehalte

Es ist deutlich schneller und zuverlässiger, automatisiert digitale Dokumente in LaTeX zu bringen, allerdings müssen einige Sachen beachtet werden:

1. Bilder enthalten in Dateien (z.B. Word, PDF) können nicht zu 100% genau extrahiert werden
2. Bei manchen Formaten kann Textformatierung (Links, Fett/Kursiv, etc.) nicht übertragen werden
3. Fehler der Artikelautoren; insbsondere Rechtschreibung oder fragwürden Textbau

Im Zweifelsfall immer die kopierten Originaldateien oder E-Mails selber überprüfen!

## In Docker ausführen

Mit Docker können alle Abhängigkeiten isoliert installiert und der Bot ausgeführt werden.

### Image Bauen

Das Image wird nun mit jeder Änderung automatisch neu gebaut und als GitHub-Package veröffentlicht.

```console
[johannes@kirby workflows]$ docker pull ghcr.io/avfrisia/frisenbrief-bot:main
main: Pulling from av-frisia/frisenbrief-bot
...
Status: Downloaded newer image for ghcr.io/avfrisia/frisenbrief-bot:main
ghcr.io/av-frisia/frisenbrief-bot:main
```

Ansonsten kann das Image auch wie gewohnt lokal mit `docker build .` gebaut werden.

### Image Ausführen

Beispiel unter Linux:

```console
[johannes@kirby frisenbrief-bot]$ docker run -it -v $(pwd)/artikel:/usr/src/app/output:z ghcr.io/avfrisia/frisenbrief-bot:main
IMAP Server: mail.stud.uni-hannover.de
E-Mail: johannes.arnold@stud.uni-hannover.de
Password: 
Ab Datum (TT-MM-JJJJ): 01-10-2021
```

- `-it` Erlaubt es, den Bot die Standardein- und Ausgaben zu verwenden. Diese werden benötigt wenn die Flags `--host`, etc. nicht verwendet werden.
- `-v $(pwd)/artikel:/usr/src/app/output` Bindet einen Ordner `artikel` an den im Image erhaltenen `/usr/src/app/output` Ordner, welcher Ziel der Ausgabe im Image ist.

_Hinweis:_ bei manchen System mit SELinux wird die [z-Flag gebraucht](https://docs.docker.com/storage/bind-mounts/#configure-the-selinux-label).

## Installation

Der Bot hat Abhängigkeiten für `antiword`, `textract`, `latexindent` und `pandoc`. Alle weiteren Python-Abhängigkeiten können über Pip oder dem `.venv` installiert werden. Empfohlen wird es, den Bot aber in Docker auszuführen.
