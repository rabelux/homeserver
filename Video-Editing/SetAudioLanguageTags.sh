#!/bin/bash
FILES=("$1"/*.mkv)
if [ -f "${FILES[0]}" ]; then
	for f in "${FILES[@]}"
	do
		echo "Processing ${f##*/}"
		mkvpropedit "${f}" --edit track:a1 --set language=ger --edit track:a2 --set language=eng
	done
else
	echo "Error: No mkv-file found. Can not continue."
fi