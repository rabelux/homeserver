#!/usr/bin/python3

#This script needs a csv-file as argument with following columns:
#-"Title":              | Title of movie
#-"TrackID":            | Number of subtitle(s) to extract. Will be increment by 2 to
#-"Subtitle Codec":     | Currently knows "vobsub" and "pgs". Prbably obsolete with higher mkvextract-version.
#-"Part File Combined": | Full path incl. filename to mkv-file

#Possible enhancement:
#Instead of manually specifying the TrackIDs it's better to parse the mkv-file.
#see https://gitlab.com/mbunkus/mkvtoolnix/-/wikis/Automation-examples#example-1-multiplex-files-change-audio-language-remove-subtitle-track

import os
import csv
import sys

subNames = ["de.forced.", "en.forced."]
extReplace = {"vob":"sub", "pgs":"sup"}
errorLog = ""
count = 0

if not(os.path.isfile(sys.argv[1]) and sys.argv[1][-3:] == 'csv'):
    print("No/wrong CSV input specified.\nUsage: " + sys.argv[0] + " pathToCsv [-e]")
    exit(1)
    
if len(sys.argv) > 2 and sys.argv[2] == "-e":
    dryrun = False
else:
    dryrun = True
    print("--------DRYRUN--------\nNo changes are being made\nAppend '-e' to execute programm without dryrun\n-----------------------")

with open(sys.argv[1], newline='') as csvfile:
    entries = sum(1 for line in csvfile if line.rstrip()) - 1
    csvfile.seek(0) #reset position
    reader = csv.DictReader(csvfile, delimiter=';')

    for row in reader:
        count += 1
        execmd = "mkvextract '" + row['Part File Combined'] + "' tracks"
        if os.path.isfile(row['Part File Combined']):
            z = 0
            IdOffset = len(row['Audio Languages'].split('-'))
            for i in row['TrackID'].split(','):
                execmd += " " + str(int(i)+IdOffset) + ":'" + row['Part File Combined'][:-3] + \
                subNames[z] + extReplace[row['Subtitle Codec'][:3]] + "'"
                z += 1
            print("[" + str(count) + "/" + str(entries) + "] " + "Executing:\n" + execmd)
            retval = 0 if dryrun else os.system(execmd)
            if retval != 0:
                errorLog += "\t" + row['Title'] + "\n"
        else:
            print ("!!! NOT FOUND: " + row['Title'])
    if errorLog:
        print("These items had non-zero return values:\n" + errorLog)
