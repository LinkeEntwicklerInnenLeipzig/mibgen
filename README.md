# Codegenerator Mitteilungsblätter

Alle Mitteilungsblätter in den pdf-Ordner legen. Möglich sind folgende Dateinamen-Formate:

* `mib-yyyy-mm.pdf` für ein MIB eines Monats eines Jahres
* `mib-yyyy-mm-mm.pdf` für ein MIB über zwei Monate eines Jahres
* `mib-yyyy-mm-yyyy-mm.pdf` für ein MIB über zwei Monate zweier Jahre

Aufrufe:
* `python3 mibgen.py` für vollständige Generierung
* `python3 mibgen.py 2016` für Generierung eines Jahres
* `python3 mibgen.py --archive` beschreibt die Archivdatei neu

Ergebnis:

Im Ordner `output` liegen die pdf-Dateien und jpeg-Dateien zum Hochladen in
die jeweiligen Ordner. Die html-Dateien enthalten den Code, der in das Typo3-System
eingefügt werden kann.

## Download des Archivs

Das bisherige Archiv kann über das shellscript `download_archive.sh` heruntergeladen
werden.
