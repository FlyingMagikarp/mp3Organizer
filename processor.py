import os
import sys
import shutil
from mp3_tagger import MP3File, VERSION_2
import time


# Globals Benchmark stuff
startTime = time.time()
counterFilesMoved = 0
counterDirectoriesCreated = 0


# Colors for log messages
class bColors:
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    ERROR = '\033[91m'


class MusicFile:
    def __init__(self, title, artist, album, genre, filename, filepath):
        self.title = title
        self.artist = artist
        self.album = album
        self.genre = genre
        self.filename = filename
        self.filepath = filepath


# adds the filepath together, moves the file and renames it
def sortFile(file, destination):
    global counterFilesMoved
    # Genre
    checkFolderAndCreate(file.genre, destination)
    destination += '/' + file.genre
    # Artist
    checkFolderAndCreate(file.artist, destination)
    destination += '/' + file.artist
    # Album
    checkFolderAndCreate(file.album, destination)
    destination += '/' + file.album
    # Move File
    try:
        shutil.move(file.filepath, destination)
        print(bColors.OKBLUE + 'Moved File: ' + destination)
        counterFilesMoved += 1
    except OSError:
        print(bColors.ERROR + 'Error when moving File: ' + file.filepath)
        print(bColors.ERROR + 'Destination: ' + destination)
    os.rename(destination+'/'+file.filename, destination+'/'+file.title+'.mp3')


# Check if folder exists, if not create it
def checkFolderAndCreate(folder, path):
    global counterDirectoriesCreated
    path += '/' + folder
    if not os.path.isdir(path):
        os.mkdir(path)
        print(bColors.OKBLUE + 'Created directory: ' + path)
        counterDirectoriesCreated += 1
    return path


# Gets the ID3 tags from the mp3 files
def generateFile(filepath):
    file = MP3File(filepath)
    file.set_version(VERSION_2)

    filename = filepath.rpartition('/')[2]
    title = file.song or filename
    artist = file.artist or 'none'
    album = file.album or 'none'
    genre = file.genre or 'none'

    title = title.replace('/', '-')
    artist = artist.replace('/', '-')
    album = album.replace('/', '-')
    genre = genre.replace('/', '-')
    return MusicFile(title, artist, album, genre, filename, filepath)


def sortFiles(sourceRoot, destinationRoot):
    content = os.listdir(sourceRoot)
    # loop the dir and process every entry
    for entry in content:
        # .DS_Store files break the script
        if entry == '.DS_Store':
            os.remove(sourceRoot+'/.DS_Store')
            continue
        filepath = sourceRoot + '/' + entry
        if os.path.isdir(filepath):
            # if it's a dir... recursion :D
            sortFiles(filepath, destinationRoot)
            os.rmdir(filepath)
            print(bColors.OKBLUE+'Removed directory: '+filepath)
        else:
            sortFile(generateFile(filepath), destinationRoot)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        srcPath = sys.argv[1]
        dstPath = sys.argv[2]
    else:
        sys.exit(bColors.ERROR + 'Error: Missing arguments expected 2 but got ' + str(
            len(sys.argv) - 1) + ". Please provide the source and destination folder")


# check if args are valid, removes trailing '/' from autocomplete
if os.path.isdir(srcPath) and os.path.isdir(dstPath):
    srcPath = srcPath.rstrip('/')
    dstPath = dstPath.rstrip('/')
    sortFiles(srcPath, dstPath)
else:
    sys.exit(bColors.ERROR + 'Error: Source or destination arguments are not folders!')

print(bColors.OKGREEN + 'DONE!')
print(bColors.OKGREEN + 'Created '+str(counterDirectoriesCreated)+' Directories')
print(bColors.OKGREEN + 'Sorted '+str(counterFilesMoved)+' Files')
time = time.time() - startTime
print(bColors.OKGREEN + 'In {:.3f} seconds'.format(time))
