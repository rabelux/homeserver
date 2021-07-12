# list durations
for i in *.mkv; do mkvinfo $i | grep "+ Duration:"; done

# extract subtitles
for i in *.mkv; do mkvextract $i tracks 3:${i%.*}.sup; done
