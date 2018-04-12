#!/bin/bash
# Author: Wojciech Michałowski

MODEL=$1
OUTPUT=$2
LABELS_COUNT=`"$FASTTEXT_PATH" dump "$MODEL" output | head -n 1 | cut -d ' ' -f 1`

i=1
while [ "$i" -le "$LABELS_COUNT" ]
do
    LABEL=`"$FASTTEXT_PATH" dump "$MODEL" dict | tail -n "$i" | head -n 1 | cut -d ' ' -f 1`
    VECTOR=`"$FASTTEXT_PATH" dump "$MODEL" output | tail -n "$i" | head -n 1`

    if [ "$OUTPUT" ]
    then
	echo "$LABEL $VECTOR" >> "$OUTPUT"

    else
	echo "$LABEL $VECTOR"
    fi

    i=$(($i + 1))
done

