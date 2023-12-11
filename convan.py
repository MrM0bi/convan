#!/usr/bin/env python3

from argparse import RawTextHelpFormatter
import argparse
import os
from posixpath import basename
import re

FFCODECS = [["g711a", "alaw"], ["g711u", "mulaw"], ["g722", None], ["opus-nb", None], ["opus-wb", None]]


# Looks up the Key in an "Map-Array" and returns the value; None if the Key is not found
def getmapkey(string, arr):
    string = str(string)

    for a in arr:
        if len(a) == 2:
            if string == str(a[0]).strip():
                return a[1]
    return None

# Returns the Full Systempath of an given File
def getfullpath(path):
    path = str(path).strip()

    if path.startswith("~/"):
        path = os.path.expanduser('~')+"/"+path[path.index("~")+2:]
    elif not path.startswith("/"):
        path = os.getcwd()+"/"+path

    return path

# Devide path into Folderpath and Filename
def splitfullpath(path):
    path = str(path).strip()

    folder = path[ : path.rindex("/")+1 ]
    name = path[path.rindex("/")+1 : ]

    return [folder, name]



quietargs = ["-loglevel quiet", "-q"]

scriptdir = os.path.dirname(os.path.realpath(__file__))
systemp = "/tmp/"


parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter, description="Mixes the audio FILEs given as arguments down to mono, then normalizes them (if -m is not specified).\nThen it converts them to sets of audio files transcoded to the most common VoIP Telephony standards g711a, g711u, g722, g729, opus-nb and opus-wb.")

parser.add_argument("file", help="One or more file(s) to convert", type=argparse.FileType('r'), nargs='+')
parser.add_argument("-n", "--name", help="Specify the name of the Sub-directory and audio files", default=None)
parser.add_argument("-o", "--outputdir", help="Specify an Output directory", default=None)
parser.add_argument("-s", "--nosubdir", help="Disables the creation of a Sub-directory; incompatible with -m", action='store_true')
parser.add_argument("-k", "--keeptmp", help="Keep all temporary files", action='store_true')
parser.add_argument("-m", "--moveog", help="Moves the original file into the subdirectory; incompatible with -s", action='store_true')
parser.add_argument("-w", "--wavonly", help="Converts given codec files to a WAV file only", action='store_true')
parser.add_argument("--del_og", help="Deletes the original file", action='store_true')
parser.add_argument("-d", "--debug", help="Show additional information and ffmpeg output", action='store_true')

args = parser.parse_args()



# Cicles through all passed files
for file in args.file:

    # Get Filename from IO-Object 
    file = file.name

    print("\n{}:\n{}".format(file, "".ljust(len(file)+1, "=")))

    # Convert into full Path
    full = getfullpath(file)

    # Split Path and Filename
    wd = os.path.dirname(full)+"/"
    fn = os.path.basename(full)

    # Saves the current Filename two times before editing
    ogfn = fn
    monoinfn = fn
    

    # Checks if the file has a valid extension
    if re.search("\.(mp3|wav|g711[au]|g72[29]|opus-[nw]b)$", ogfn, re.IGNORECASE) is not None:
        
        # Removes the File extension
        fn = re.sub("\..+", "", fn)


        # Rename ouput file if argument is given
        if args.name is not None:
            fn = str(args.name).strip()


        # Specify the output directories 
        tmpdir = wd
        outdir = wd+fn+"/"
        monoindir = wd


        # Change Output directory if argument is present
        if args.outputdir is not None:
            fullout = getfullpath(args.outputdir)
            outdir = os.path.dirname(fullout)+"/"+fn+"/"


        if args.nosubdir:
            outdir = outdir[ : outdir.rindex("/", 0, -1)+1]


        converttowavfirst = False

        # If input file is not a mp3 or wav but one of the supported codecs, convert it to wav first
        if re.search("\.(g711[au]|g72[29]|opus-[nw]b)$", ogfn, re.IGNORECASE) is not None:
            converttowavfirst = True
            
            ext = ogfn[ ogfn.rindex(".") : ]
            ffcodec = getmapkey(ext[1:], FFCODECS)

            if ffcodec is None:
                os.system("ffmpeg -y {} -i {} {}".format(quietargs[0], wd+ogfn, tmpdir+fn+"_wav.wav"))
            else:
                os.system("ffmpeg -y {} -f {} -ar 8000 -i {} {}".format(quietargs[0], ffcodec, wd+ogfn, tmpdir+fn+"_wav.wav"))
            print("  -> Convert \"{}\" to \".wav\"".format(ext))

            monoinfn = fn+"_wav.wav"
            monoindir = tmpdir


        if not args.wavonly:

            # Remove Quiet Flags if debug arg is present
            if args.debug:
                quietargs = ["", ""]


            # Mixes Stereo down to Mono
            os.system("ffmpeg -y {} -i {} -vn -b:a 192k -ac 1 {}_mono.mp3".format(quietargs[0], monoindir+monoinfn, tmpdir+fn))
            print("  -> Mixed Stereo down to Mono")

            # Normalises Audio
            os.system("ffmpeg-normalize {1}_mono.mp3 -c:a mp3 -b:a 192k {0} -f -o {1}_norm.mp3".format(quietargs[1], tmpdir+fn))
            print("  -> Normalized Audio")


            if not args.keeptmp:
                os.remove(tmpdir+fn+"_mono.mp3")

                if converttowavfirst:
                    os.remove(tmpdir+fn+"_wav.wav")


            if not args.nosubdir and not os.path.exists(outdir):
                os.mkdir(outdir)
                print("  -> Created Folder: \'{}\'".format(fn))
            
            print("  -> Output location: \'{}\'".format(outdir))

            os.system("ffmpeg -y {} -i {} -f alaw -ar 8000 {}".format(quietargs[0], wd+fn+"_norm.mp3", outdir+fn+".g711a"))
            print("  -> Converted to g711a")

            os.system("ffmpeg -y {} -i {} -f mulaw -ar 8000 {}".format(quietargs[0], wd+fn+"_norm.mp3", outdir+fn+".g711u"))
            print("  -> Converted to g711u")

            os.system("ffmpeg -y {} -i {} -f g722 -ar 16000 {}".format(quietargs[0], wd+fn+"_norm.mp3", outdir+fn+".g722"))
            print("  -> Converted to g722")

            os.system("ffmpeg -y {0} -i \"{1}\" -f s16le -c:a pcm_s16le -ar 8000 -ac 1 \"{2}\"; python3 \"{3}/g729a.py\" encode \"{2}\" \"{4}\"".format(quietargs[0], wd+fn+"_norm.mp3", systemp+"convan_pcm_temp.wav", scriptdir, outdir+fn+".g729"))
            print("  -> Converted to g729")

            os.system("ffmpeg -y {} -i {} -f opus -ar 48000 -b:a 20000 -vbr on {}".format(quietargs[0], wd+fn+"_norm.mp3", outdir+fn+".opus-wb"))
            print("  -> Converted to opus-wb")

            os.system("ffmpeg -y {} -i {} -f opus -ar 48000 -b:a 12000 -vbr on {}".format(quietargs[0], wd+fn+"_norm.mp3", outdir+fn+".opus-nb"))
            print("  -> Converted to opus-nb")

            if not args.keeptmp:
                os.remove(tmpdir+fn+"_norm.mp3")

            if args.del_og:
                os.remove(wd+ogfn)
            elif args.moveog and not args.nosubdir:
                os.rename(wd+ogfn, outdir+ogfn)

        else:
            if not converttowavfirst:
                print("  [ERROR] A file with one of the following extensions has to be given:")
                print("          g711a, g711u, g722, g729, opus-nb or opus-wb")
                quit()
    
    else:
        print("  [ERROR] Invalid extension found: \'{}\'".format(re.search("\.\w+$", ogfn).group(0)))