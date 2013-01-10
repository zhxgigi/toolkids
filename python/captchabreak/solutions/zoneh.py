#!/usr/bin/env python
from preprocess import *
from base import BaseClassifier
from classify import Classifier
from itertools import chain
import cPickle as pickle
import random

class ZonehcnClassifier(BaseClassifier):
    name = "zonehcn"
    def __init__(self, modeldir=None):
        BaseClassifier.__init__(self, modeldir)
        self.classes = 46
        self.class_sample_num = 5
        self.sample_size = 15#15*15
        self.model = None
        self.model_type = 1 #1=knearest, 2=svm
        self.k_neighbor_num = 5
    
    def segment(self, filepath):
        src_img = self._load_image(filepath)
        img_chunks = vertical_segment(src_img)
        img_chunks = filter(lambda x : count_pixels(x) > 20, img_chunks)
        assert len(img_chunks) == 4, 'segment image failed!'
        return img_chunks
    
    def _load_image(self, path):
        """load image by using some basic preprocess"""
        srcimg = cv.LoadImage(path, 0)
        cv.Threshold(srcimg, srcimg, 100, 255, cv.CV_THRESH_BINARY)
        return srcimg

def segment_catpcha_to_singlechar():
    captchadir = r'D:\projects\python\xunworks\captchabreak\data\zoneh\pics'
    outputdir =  r'D:\projects\python\xunworks\captchabreak\data\zoneh\pics_singlechar'
    try:
        os.mkdir(outputdir)
    except:
        pass
    
    segmentor = ZonehSegmentor()
    count = 0
    for fpath in walkdir(captchadir):
        
        imgs = segmentor.segment(fpath)
        for img in imgs:
            outputfile = os.path.join(outputdir, 'zoneh_%d.jpg'%count)
            count += 1
            cv.SaveImage(outputfile, img)

def classify_singlechar():
    traindata = r'D:\projects\python\xunworks\captchabreak\data\zoneh\trainning'
    outdir = r'D:\projects\python\xunworks\captchabreak\data\zoneh\pics_singlechar_classify'
    
    toclassify_data = r'D:\projects\python\xunworks\captchabreak\data\zoneh\pics_singlechar'
    try:
        os.makedirs(outdir)
    except:
        pass
    
    segmentor = ZonehSegmentor()
    segmentor.train(traindata)
    
    filepaths = []
    for path in walkdir(toclassify_data):
        filepaths.append(path)
    count = 0
    for i in range(100, 200):
        path = filepaths[i]
        img = segmentor.load_image(path)
        label = int(segmentor.classify(img)[0])
        try:
            os.makedirs(os.path.join(outdir, str(label)))
        except:
            pass
        
        outputfile = os.path.join(outdir, str(label), '%d.jpg'%count)
        cv.SaveImage(outputfile, img)
        count += 1

def classify_captcha():
    traindir = r'D:\projects\python\xunworks\captchabreak\data\zoneh\trainning'
    zcn = ZonehcnClassifier()
    zcn.model_type = 1
    zcn.train(traindir)
    zcn.write_modeldata()
    zcn.load_modeldata()
    
    captchar_dir = r'D:\projects\python\xunworks\captchabreak\data\zoneh\pics'
    filepaths = []
    for root, dirs, files in os.walk(captchar_dir):
        for file in files:
            path = os.path.join(root, file)
            filepaths.append(path)
    count = 0
    for i in range(100, 200):
        path = filepaths[i]
        ret = zcn.classify_captcha(path)
        print ret
        img = cv.LoadImage(path)
        cv.ShowImage('c', img)
        cv.WaitKey()
        
    
if __name__ == '__main__':
    #segment_catpcha_to_singlechar()
    #classify_singlechar()
    classify_captcha()