#!/usr/bin/python3

import os
import os.path as path
import argparse
from datetime import date
from collections import namedtuple, defaultdict
from itertools import product

Entry = namedtuple('Entry', ('pdf', 'img', 'subtitle'))

months = '', 'Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'
baseurl = 'fileadmin/leipzig/dokumente/Mitteilungsblatt/'
domain = 'http://beta4.soziales-sachsen.de/'
columns = 3

def get_pdfnames(pdfpath):
    import re
    pdf_regex = re.compile(r'^mib(-\d{4}(-\d{2})+)+\.pdf$', flags=re.IGNORECASE)
    return (path.join(pdfpath, f) for f in os.listdir(pdfpath) if pdf_regex.match(f))

def get_subtitle(filename):
    s = filename[4:-4]
    d = defaultdict(list)
    year = ''
    for e in s.split('-'):
        if len(e) == 4:
            year = e
        if len(e) == 2:
            d[year].append(e)
    return ' / '.join('/'.join(months[int(m)] for m in sorted(d[y])) + ' ' + y for y in sorted(d.keys()))


def copy_pdf(pdffile, outputpath):
    import shutil
    return shutil.copy(pdffile, outputpath)

def generate_thumbnail(pdffile, outputpath):
    # convert -thumbnail 150x -background white -alpha remove "$FILE"[0] "${FILE}.jpg"
    import subprocess
    target_filename = path.join(outputpath, path.basename(pdffile)) + '.jpg'
    subprocess.call(['convert', '-thumbnail', '150x', '-background', 'white',
                        '-alpha', 'remove', pdffile + '[0]', target_filename])
    return target_filename

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--archive', action='store_const', const=True, help='Archiv neu generieren')
    parser.add_argument('year', nargs='?', type=int, help='Jahr')
    args = parser.parse_args()

    # read path/construct
    basepath = path.dirname(path.abspath(__file__))
    pdfpath = path.join(basepath, 'pdf')
    outputpath = path.join(basepath, 'output')
    archivefile = path.join(basepath, 'archive')

    years = [args.year] if args.year else list(range(2005, date.today().year + 2))

    # collect
    items_in_year = defaultdict(list)
    for pdffile, year in product(get_pdfnames(pdfpath), years):
        if str(year) in path.basename(pdffile):
            items_in_year[year].append(pdffile)

    archive = []

    for year in items_in_year:
        yearpath = path.join(outputpath, str(year))
        os.makedirs(yearpath, exist_ok=True)

        entries = []

        for item in sorted(items_in_year[year], key=lambda v: v.upper(), reverse=True):
            pdf = copy_pdf(item, yearpath)
            img = generate_thumbnail(item, yearpath)
            entries.append(Entry(pdf=path.basename(pdf),
                                img=path.basename(img),
                                subtitle=get_subtitle(path.basename(pdf))
                                ))

        html_rows = []
        for i, entry in enumerate(entries):
            row = (i // columns) * 2
            while len(html_rows) <= row + 1:
                html_rows.append([])
            folder = baseurl + str(year) + '/'
            html_rows[row].append('<td style=\"text-align: center\"><link ' + folder + entry.pdf +' - download \"Leitet Herunterladen der Datei ein\"><img src=\"' + folder + entry.img + '\" /></link></td>')
            html_rows[row + 1].append('<td style=\"text-align: center\">' + entry.subtitle + '</td>')

        for row in html_rows:
            while len(row) < columns:
                row.append('<td></td>')

        html = '<table summary=\"Mitteilungsblätter '+ str(year) +'\"><tbody>\n<tr>' + '</tr>\n<tr>'.join('\n'.join(r) for r in html_rows) + '</tr>\n</tbody></table>\n'
        html_file = path.join(yearpath, str(year) + '.html')
        with open(html_file, 'w') as f:
            f.write(html)

        if args.archive:
            for entry in entries:
                archive.append(domain + baseurl + str(year) + '/' + entry.pdf)

    if args.archive:
        with open(archivefile, 'w') as af:
            af.write('\n'.join(sorted(set(archive))))

if __name__ == "__main__":
    main()
