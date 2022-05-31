# convan
Converts audio files to the most common VoIP Telephony standards g711a, g711u, g722, g729, opus-nb and opus-wb

<pre>
usage: convan [-h] [-n NAME] [-o OUTPUTDIR] [-s] [-k] [-m] [--del_og] [-d] file [file ...]

Mixes the audio FILEs given as arguments down to mono then normalizes them (if -m is not specified).
Then it converts them to sets of audio files transcoded to the most common VoIP Telephony standards g711a, g711u, g722, g729, opus-nb and opus-wb.

positional arguments:
  file                  One or more file(s) to convert

optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  Specify the name of the Sub-directory and audio files
  -o OUTPUTDIR, --outputdir OUTPUTDIR
                        Specify an Output dirrectory
  -s, --nosubdir        Disables the creation of a Sub-directory; incompatible with -m
  -k, --keeptmp         Keep all temporary files
  -m, --moveog          Moves the original file into the subdirectory; incompatible with -s
  --del_og              Deletes the original file
  -d, --debug           Show additional information and ffmpeg output
  </pre>

