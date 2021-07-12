#!/bin/bash
# Prove two paths as argument. First path is the video-source, second is the subtitle-source. Both paths need same amount of files in mkv-format.

FILES=("$1"/*.mkv)
SUB_SOURCES=("$2"/*.mkv)
i=0
if [ ! -f "${FILES[0]}" ]; then
	echo "No subtitle source found"
fi
if [ -f "${FILES[0]}" ]; then
	for f in "${FILES[@]}"
	do
		echo  "Replace Subs of ${f##*/} with ${SUB_SOURCES[i]##*/}?"
		select opt in yes skip abort; do
			case $opt in
				yes )	echo "Creating GOT_S03E0$((i+1)).mkv"; break;;
				skip )	((i++)); continue;;
				*)		exit;;
			esac
		done
		mkvmerge -o GOT_S03E$(printf "%02d" $((i+1))).mkv -S "${f}" --no-audio --no-video --no-chapters "${SUB_SOURCES[i]}"
		((i++))
	done
else
	echo "Error: No movie-source found. Can not continue."
fi
