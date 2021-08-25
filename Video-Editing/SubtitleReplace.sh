#!/bin/bash
# Provide two paths and the output-name-prefix as argument. First path is the video-source, second is the subtitle-source. Both paths need same amount of files in mkv-format.
# Third argument is something like "GOT_S01E" and will end up in "GOT_S01Exx.mkv

#set -x

usage() {
    echo "This script replaces subtitles of mkv-files in one folder with subtitles of mkv-files in another folder."
	echo "Input arguments: Path to video-source, path to subtitle-source, Namescheme of output files like GOT_S01E"
    echo "Usage: /path/to/SubtitleRaplace.sh /path/to/source /path/to/subtitles GOT_S01E"
	exit
}

## Catch wrong inputs
if [[ ! -d "$1" || ! -d "$2" ]]; then
	echo "Abort: Provided path not found"
	usage
elif [[ $# -eq 8 ]]; then
	echo "Abort: Invalid amount of arguments"
	usage
fi

VID_SOURCE=("$1"/*.mkv)
SUB_SOURCE=("$2"/*.mkv)

if [[ ${#VID_SOURCE[@]} -ne ${#SUB_SOURCE[@]} ]] || [[ ${#VID_SOURCE[@]} -eq 0 ]] ; then
	echo "Abort: Provided directories do not have same amount of files"
	exit 1
fi


## Now do stuff

i=0
all=false
for f in "${VID_SOURCE[@]}"
do
	if [ "$all" = false ]; then
		echo "Replace Subs of ${f##*/} with ${SUB_SOURCE[i]##*/}?"
		echo "Source $(mkvinfo "${f}" | grep "+ Duration:" | cut -c 5-)"
		echo "Target $(mkvinfo "${SUB_SOURCE[i]}" | grep "+ Duration:" | cut -c 5-)"
		select opt in yes "yes for all" skip abort; do
			case $opt in
				yes )			echo "Creating GOT_S03E0$((i+1)).mkv"; break;;
				"yes for all" ) all=true; break;;
				skip )			((i++)); continue;;
				*)				exit;;
			esac
		done
	fi
	mkvmerge -o "$3""$(printf "%02d" $((i+1)))".mkv -S "${f}" --no-audio --no-video --no-chapters "${SUB_SOURCE[i]}"
	((i++))
done
