# MP3 TO MP3 CONVERSION SCRIPT
# script to convert mp3 files to mp3 audio
#
# usage: python mp3tomp3_m32.py [input directory [output directory]]
# input directory (optional)
# output directory (optional)
#
# install lame
# install python2.7


from subprocess import call     # for calling mplayer and lame
from sys import argv            # allows user to specify input and output directories
import os                       # help with file handling

def check_file_exists(directory, filename, extension):
    path = directory + "/" + filename + extension
    return os.path.isfile(path)

def main(indir, outdir):


    try:
        # check specified folders exist
        if not os.path.exists(indir):
            exit("Error: Input directory \'" + indir + "\' does not exist. (try prepending './')")
        if not os.path.exists(outdir):
            exit("Error: Output directory \'" + outdir + "\' does not exist.")
        if not os.access(outdir, os.W_OK):
            exit("Error: Output directory \'" + outdir + "\' is not writeable.")

        print ("[%s/*.mp3] --> [%s/*.mp3]" % (indir, outdir))
        files = [] # files for exporting

        # get a list of all convertible files in the input directory
        filelist = [ f for f in os.listdir(indir) if f.endswith(".mp3") ]
        for path in filelist:
            basename = os.path.basename(path)
            filename = os.path.splitext(basename)[0]
            files.append(filename)
        # remove files that have already been outputted from the list
        files[:] = [f for f in files if not check_file_exists(outdir, f, ".mp3")]
    except OSError as e:
        exit(e)

    if len(files) == 0:
        exit("Could not find any files to convert that have not already been converted.")

    # convert all unconverted files
    for filename in files:
        print ("-- converting %s.mp3 to %s.mp3 --" % (indir + "/" + filename, outdir + "/" + filename))
        call(["lame", "-m", "m", "-b", "32", "--mp3input", indir + "/" + filename + ".mp3" , outdir + "/" + filename + ".mp3"])

# set the default directories and try to get input directories
args = [".", "."]
for i in range(1, min(len(argv), 3)):
    args[i - 1] = argv[i]

# if only input directory is set, make the output directory the same
if len(argv) == 2:
    args[1] = args[0]

main(args[0], args[1])
