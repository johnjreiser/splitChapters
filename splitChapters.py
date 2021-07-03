#!/usr/bin/env python3

import os
import json
import ffmpeg
import time
import logging

logging.basicConfig(level=logging.DEBUG)


def parseChapter(c, ext=".mp4"):
    f = {"id": c["id"], "title": None}
    if "tags" in c and "title" in c["tags"]:
        f["title"] = c["tags"]["title"]
    f["filename"] = "{:0>4}{}{}".format(f["id"], f["title"].replace(" ", "_"), ext)

    time_base = eval(c["time_base"])

    f["start_time"] = time.strftime(
        "%H:%M:%S", time.gmtime(int(float(c["start"]) * time_base))
    )
    f["end_time"] = time.strftime(
        "%H:%M:%S", time.gmtime(int(float(c["end"]) * time_base))
    )
    return f


def getChapterData(filename):
    ext = os.path.splitext(filename)[1]
    data = ffmpeg.probe(filename, show_chapters=None)
    chapter_data = []
    for x in data["chapters"]:
        chapter_data.append(parseChapter(x, ext))
    return chapter_data


def timeTupleToSeconds(t):
    if isinstance(t, str):
        t = time.strptime(t, "%H:%M:%S")
    s = (t.tm_hour * 3600) + (t.tm_min * 60) + t.tm_sec
    logging.debug((t, s))
    return s


def exportClip(infile, outfile, sTime, eTime):
    logging.debug((infile, outfile, sTime, eTime))
    steps = (
        ffmpeg.input(infile).output(outfile, **{"vsync": 0, "ss": sTime, "to": eTime})
        #        .trim(start=sTime, end=eTime)
        #        .output(outfile, **{"vsync": 0})
    )

    logging.debug(steps.compile())
    steps.run()


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser(
        description="Review chapters in video file and split on markers."
    )
    p.add_argument("filename", help="Video Filename")
    p.add_argument(
        "-c",
        "--chapters",
        default=False,
        help="Print chapter markers and exit.",
        action="store_true",
    )
    p.add_argument(
        "-o", "--override", default=False, help="Specify override marker file."
    )

    args = p.parse_args()
    if args.chapters:
        print(json.dumps(getChapterData(args.filename), indent=2))
    else:
        if args.override:
            with open(args.override, "r") as fh:
                data = json.load(fh)
        else:
            data = getChapterData(args.filename)
        for x in data:
            logging.debug(x)
            if not os.path.exists(x["filename"]):
                exportClip(args.filename, x["filename"], x["start_time"], x["end_time"])
