# splitChapters

A Python script to aid in splitting long video files into individual files based off of chapter markers. 

Some video conferencing platforms (e.g. Zoom) allow for a meeting to be recorded. The resulting video file includes chapter markers based on when screen sharing begins and ends. This script can help split long meetings into a set of files representing individual presentations within the meeting. 

The script can split directly based on the markers within the file, or from an override file. You can create the override file from the script and then manually edit. This may be useful if you'd want multiple chapters contained in a single file instead of separate files. 

## Pre-requisites

- [Python 3](https://python.org)
- [ffmpeg](https://ffmpeg.org/)
- [ffmpeg-python](https://github.com/kkroening/ffmpeg-python)

## Usage

    usage: splitChapters.py [-h] [-c] [-o OVERRIDE] filename

    Review chapters in video file and split on markers.

    positional arguments:
       filename              Video Filename

    optional arguments:
      -h, --help            show this help message and exit
      -c, --chapters        Print chapter markers and exit.
      -o OVERRIDE, --override OVERRIDE
                            Specify override marker file.

## License

MIT License; use at your own risk.