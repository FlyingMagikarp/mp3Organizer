# mp3 Organizer
This python scripts moves all .mp3 files in a source folder to a destination with a directory structure like this

    .
    └──<genre>
       └──<artist>
          └──<album>



It also renames the track to only the song name (without artist).

It gets all the needed information from ID3-tags. Only works with ID3 V2.0+
If a ID3 tag is empty, it gets replaced by the default value "none"


## Arguments
The script takes 2 arguments: Source & Destination. Both are ***relative*** paths to the respective directories.

The Script will loop through the source directory, move the files and delete empty subdirectories(except the source itself)


## Example
We have a Music directory with the script, a dump directory and a collection directory. In the Music directory there's a file called 'Prok & Fitch - Indiance.mp3'

    Music
        ├── _collection
        ├── _dump
        │    └──Tech House
        │       └──Prok & Fitch - Indiance.mp3
        └── processor.py

Call the script with these args:

    python3 processor.py dump/ collection/

The result should be this structure:

    Music
        ├── _collection
        │    └──Tech House
        │        └──Prok & Fitch
        │            └──Indiance  <--- it's the album :)
        │               └──Indiance(Original Mix).mp3
        ├── _dump
        └── processor.py