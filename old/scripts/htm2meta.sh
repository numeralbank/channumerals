#!/usr/bin/env bash

WDIR="/Users/bibiko/Documents/MPI/Colleagues/Numerals/new"

OUTFILELANG="/Users/bibiko/Documents/MPI/Colleagues/Numerals/lang_new.tab"
OUTDIRHTML="/Users/bibiko/Documents/MPI/Colleagues/Numerals/htm"

STARTLANGIDX=1

cd "$WDIR"

echo -e "NAME\tLAND\tISO\tGLOTTO_NAME\tGLOTTO_CODE\tFILE\tAUDIO\tSOURCE\tNR_DATASETS" > "$OUTFILELANG"

for f in *.htm
do
	echo "$f"
	HCH=`textutil -stdout -convert html "$f"`
	CH=`echo -e "$HCH" | grep -F 'Language name and location'`
	if [ -z "$CH" ]; then
		continue
	fi
	CH=`echo -e "$HCH" | grep -F 'Questionnaire'`
	if [ -n "$CH" ]; then
		continue
	fi

	echo -e "$HCH" > "$OUTDIRHTML/$f"

	LG=$(cat "$OUTDIRHTML/$f" | perl -pe 's/<span[^>]*?>//g;s/<\/span>//g;' | grep -F 'Language name and location' | perl -pe 's/^.*?Language name and location[\s:ː]*(.*)/$1/;s/<\/span>//g;s/ / /g')
	LG=$(echo "$LG" | perl -pe 's/^.*?<\/i>\s*<\/b>\s*<\/p>\s*$//') # questionnaire

	DATASETS=$(($(echo "$LG" | wc -l) + 0 ))
	
	NAMELAND=$(echo "$LG" | head -n 1 | perl -pe 's/<[^>]*?>//g; s/^\s*([^,]*?)\s*,\s*(.*?)\s*\[.*/$1~$2/;s/^\s*//g;s/\s*~\s*/~/g;s/ {2,}/ /g;s/ ,/,/g;s/\s*$//g;')
	NAME=$(echo "$NAMELAND" | perl -pe 's/^\s*(.*?)\s*~.*/$1/;s/\s*\[.+?\]\s*$//')
	LAND=$(echo "$NAMELAND" | perl -pe 's/^.*?~\s*(.*)\s*/$1/;s/\s*\[.+?\]\s*$//')
	
	if [ "$NAME" == "$LAND" ]; then
		LAND="zzCHECK_COUNTRY"
	fi

	ISO=$(echo "$LG" | head -n 1 | perl -pe 's/^.*?[=\/]([a-z]{2,3})".*/$1/;s/^\s*//g;s/\s*$//g;')
	ISOLEN=${#ISO}
	if [ $ISOLEN -gt 3 ]; then
		ISO=""
	fi
	if [ $ISOLEN -lt 2 ]; then
		ISO=""
	fi

	GLCODE=""
	GLNAME=""

	if [ -n "$ISO" ]; then
		GLD=`cat ../script/glottolog_iso.tab | egrep "^$ISO\b"`
		if [ -n "$GLD" ]; then
			GLNAME=`echo "$GLD" | cut -f 2`
			GLCODE=`echo "$GLD" | cut -f 3`
		fi
	fi

	textutil -stdout -convert txt "$OUTDIRHTML/$f" | perl -pe 's/ / /g' > /tmp/numtxt.txt

	AUDIO=$(cat "$f" | grep -F '<audio' | perl -pe 's/^.*?src=\s*["\x{27}](.*?)["\x{27}].*/$1/' | tr '\n' '; ')

    for i in `seq 1 $DATASETS`;
    do
		SOURCE=$(cat /tmp/numtxt.txt | grep -F 'Linguist providing data' | head -n $i | tail -n 1 | perl -pe 's/ː/:/g;s/^.*?:\s*(.*)/$1/;s/ +/ /g;s/^\s*//;s/\s*$//;s/ ,/,/g;')
		if [ -z "$SOURCE" ]; then
			SOURCE=$(cat /tmp/numtxt.txt | grep -F 'Data source' | head -n $i | tail -n 1 | perl -pe 's/ː/:/g;s/^.*?:\s*(.*)/$1/;s/ +/ /g;s/^\s*//;s/\s*$//;s/ ,/,/g;')
		fi
		SOURCE=$(echo -e "$SOURCE" | perl -pe 's/ 提供.*$//;s/ /; /g')
		echo -e "$NAME\t$LAND\t$ISO\t$GLNAME\t$GLCODE\t$f\t$AUDIO\t$SOURCE\t$DATASETS\t$i" | perl -pe 's/ +\t/\t/g;s/\t +/\t/g;s/ {2,}/ /g' >> "$OUTFILELANG"
	done
done

rm -f /tmp/numtxt.txt
