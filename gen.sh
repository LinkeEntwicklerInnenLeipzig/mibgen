FOLD=$1
YEAR=$2

cols=3

cd $FOLD

echo "<table summary=\"\"><tbody>"

for COUNT in $(seq 1 12); do
    let "m=COUNT % cols"
    [ $m == 1 ] && echo "<tr>"
    FILE=`ls *.pdf | head -n $COUNT | tail -n 1`
    convert -thumbnail 150x -background white -alpha remove "$FILE"[0] "${FILE}.jpg"
    ([ ! -z $FILE ] && echo "<td><link fileadmin/leipzig/dokumente/Mitteilungsblatt/${YEAR}/${FILE} - download \"Leitet Herunterladen der Datei ein\"><img src=\"fileadmin/leipzig/dokumente/Mitteilungsblatt/${YEAR}/${FILE}.jpg\" /></link></td>") || (echo "<td></td>")
    [ $m == 0 ] && echo "</tr><tr>" && (yes "<td style=\"text-align: center\">Monat ${YEAR}</td>" | head -n $cols ) && echo "</tr>" 
done

echo "</tbody></table>"
