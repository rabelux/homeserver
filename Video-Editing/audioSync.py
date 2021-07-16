#Usage: audioSync --keep-pitch input1 input2
## This script expects two inputs. First is video source, second is audio source with at least 2 audio tracks
## Requires JP

#parse input params
if $1 == "keep-pitch":
    keep_pitch = true
elif $1 == "offset-only":
    offset_only = true

#check if files exist

#check if file 2 has at least 2 audio tracks

#get tracknumbers of audiotracks in files
    trackno1_1 = getrackno(input1)(0)
    if trackno1_1 == []:
        throw exception "no audio found in input1"
    trackno2 = getrackno(input2)
    if trackno2.len < 2:
        throw exception "less than 2 audio tracks found in input2"        
    trackno2_1 = trackno2(0)
    trackno2_2 = trackno2(1)

#check if files have same framerate
conv_fr = False
if input1.fps != input2.fps
    conv_fr = True
    mkvextract $input2 tracks trackno2_2:3.mka
#extract first audio track of each file
mkvextract input1 tracks trackno1_1:1.mka
mkvextract input2 tracks trackno2_1:2.mka

#Change framerate if necessary
audiopath = "2.mka"
if conv_fr:
    #do conv fr
    if keep_pitch:
        #convert with same pitch
        conv_with(2.mka, 2_conv.mka)
        if !offset_only:
            conv_with(3.mka, 3_conv.mka)        
    else
        #convert with changed pitch
        conv_wo(2.mka, 2_conv.mka)
        if !offset_only:
            conv_wo(3.mka, 3_conv.mka)
    audiopath = 2_conv.mka

#find offset
offset = findoffset(1.mka, audiopath)
print "offset of " + offset + " ms for file " + input1

#merge files
if !offset_only:
    mergecmd = "mkvmerge -o input1_merged.mkv input1 "
    if conv_fr:
        mergecmd += "lang=eng --offset=$offset 3_conv.mka"
    else:
        mergecmd += "--no-video --no-subtitles --audiotrack:trackno2_2 --offset=$offset --lang:trackno2_2=eng $input2"
    exec (mergecmd)

#cleanup
rm --noerror 1.mka 2.mka 2_conv.mka 3.mka 3_conv.mka





getrackno(infile){
    result_str = mkvmerge -i infile | find "audio"
    retval = []
    for each line in result_str:
        retval.append(line[-2])
    return retval
}