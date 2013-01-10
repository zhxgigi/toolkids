#!/usr/bin/env python

import cv
import os
import sys

def audit():
    segdir = r"D:\projects\python\xunworks\captchabreak\data\zoneh.org\seg"
    outputdir = r'D:\projects\python\xunworks\captchabreak\data\zoneh.org\audit'
    
    count = 0
    
    for root, dir, files in os.walk(segdir):
        for file in files:
            fullpath = os.path.join(root, file)
            img = cv.LoadImage(fullpath)
    
            cv.ShowImage('char', img)
                    
            cv.WaitKey()
            img_char = ""
            while not img_char:
                img_char = raw_input('enter img char: ')
                        
            output_path = os.path.join(outputdir, img_char.lower())
            if not os.access(output_path, os.F_OK):
                os.makedirs(output_path)
            fname = "%s_%d.jpg" % (img_char, count)
            count += 1
            output_fullpath = os.path.join(output_path, fname)
            cv.SaveImage(output_fullpath, img)
            os.remove(fullpath)
            cv.DestroyWindow("char")

import shutil
def rename(datadir, outdir):
    catecount = 0
    for root, dir, files in os.walk(datadir):
        filenum = len(files)
        if not filenum:
            continue
        subfix = 0
        
        
        for file in files:
            path = os.path.join(root, file)
            cate = path.split(os.sep)[-2]
            newfilename = "%s_%d.jpg" % (catecount, subfix)
            newpath = os.path.join(outdir, newfilename)
            shutil.copy(path, newpath)
            subfix += 1
        catecount += 1
            
def load_data(datadir):
    classes = os.listdir(datadir)


import shutil
def rename2(datadir, outdir):
    count = 0
    from collections import defaultdict
    holder = defaultdict(list)
    for root, dirs, files in os.walk(datadir):
        for fname in files:
            filepath = os.path.join(root, fname)
            cate = filepath.split(os.sep)[-2]
            holder[ord(cate)].append(filepath)
    
    for dirname in holder.keys():
        path = os.path.join(outdir, str(dirname))
        try:
            os.makedirs(path)
        except Exception, e:
            print str(e)
        
    count = 0
    for dirname, files in holder.iteritems():
        for fpath in files:
            newfname = "%s_%d.jpg" % (chr(dirname), count)
            newpath = os.path.join(outdir, str(dirname), newfname)
            shutil.copy(fpath, newpath)
            count += 1
        

if __name__ == '__main__':
    #audit()
    
    src = r'D:\projects\python\xunworks\captchabreak\data\zoneh.org\audit'
    dst = r'D:\projects\python\xunworks\captchabreak\data\zoneh.org\rename'
    rename2(src, dst)
    #