# convan
Converts audio files to the most common VoIP Telephony standards g711a, g711u, g722, g729, opus-nb and opus-wb

### Dependencies
The Script needs [ffmpeg](https://github.com/FFmpeg/FFmpeg) and [slhck/ffmpeg-normalize](https://github.com/slhck/ffmpeg-normalize) to be installed on the system.
If you are running Python 3.5 you can use the modified version of slhck/ffmpeg-normalize included in this repo.
To convert to G.729 a slightly modified version of [g729a-python](https://github.com/AlexIII/g729a-python/tree/master) is needed. But this is also already included in this repo.

### Usage
<pre>
usage: convan [-h] [-n NAME] [-o OUTPUTDIR] [-s] [-k] [-m] [-w] [--del_og] [-d] file [file ...]

Mixes the audio FILEs given as arguments down to mono, then normalizes them (if -m is not specified).
Then it converts them to sets of audio files transcoded to the most common VoIP Telephony standards g711a, g711u, g722, g729, opus-nb and opus-wb.

positional arguments:
  file                  One or more file(s) to convert

options:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  Specify the name of the Sub-directory and audio files
  -o OUTPUTDIR, --outputdir OUTPUTDIR
                        Specify an Output directory
  -s, --nosubdir        Disables the creation of a Sub-directory; incompatible with -m
  -k, --keeptmp         Keep all temporary files
  -m, --moveog          Moves the original file into the subdirectory; incompatible with -s
  -w, --wavonly         Converts given codec files to a WAV file only
  --del_og              Deletes the original file
  -d, --debug           Show additional information and ffmpeg output
  </pre>

