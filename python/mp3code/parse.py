#!/usr/bin/env python
#encoding:utf8

from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import os
import sys

def renameMp3(filename, count=0):
    audio = MP3(filename, ID3=EasyID3)
    print "before: %s" % audio
    new_filename = filename[-7:]
    num = int(new_filename[-7:-4]) + count
    new_title = "SuiTangYanYi_%d" % num
    artist = "STF"
    album = "SuiTangYanYi"
    audio['album'] = album
    audio['artist'] = artist
    if 'tracknumber' in audio:
        del audio['tracknumber']
    audio['title'] = new_title
    audio.save()
    print "after: %s" % audio



if __name__ == '__main__':
    ddir = "/Users/hongxun/Desktop/上"
    for root, dirs, files in os.walk(ddir):
        for fname in files:
            fpath = os.path.join(root, fname)
            #renameMp3(fpath, count=116)
            renameMp3(fpath, count=0)
