#!/usr/bin/env python
from preprocess import *
from base import BaseClassifier
import cPickle as pickle
import random
import os

class ZonehorgClassifier(BaseClassifier):
    name = "zonehorg"
    def __init__(self, classes=24, samplepercls=10, modeltype=1, modeldir=None):
        BaseClassifier.__init__(self, modeldir)
        
        self.classes = classes
        self.class_sample_num = samplepercls
        
        self.model_type = modeltype #1=knearest, 2=svm
        self.k_neighbor_num = 5
        self.sample_size = 15#15*15
        
        self.model = None
        
    def _load_image(self, path):
        """load image by using some basic preprocess"""
        srcimg = cv.LoadImage(path, 0)
        cv.Threshold(srcimg, srcimg, 40, 255, cv.CV_THRESH_BINARY)
        return srcimg

    def segment(self, filepath):
        image = self._load_image(filepath)
        
        img_cf2, p = color_filling2(image, 10, 6)
        
        #img_chunks, p = color_filling(img_cf2, 20)
        img_chunks = vertical_segment(img_cf2)
        img_chunks = filter(lambda x : count_pixels(x) > 20, img_chunks)
        #assert len(img_chunks) == 5, "classify failed!"
        
        #cv.ShowImage('orgin', image)
        #cv.ShowImage('cf2', img_cf2)
        #for i in range(len(img_chunks)):
        #    cv.ShowImage('vs_%d'%i, img_chunks[i])
        #cv.WaitKey()
        return img_chunks
    
def segment_to_char():
    datapath = r'D:\projects\python\xunworks\captchabreak\data\zoneh.org\train'
    output = r'D:\projects\python\xunworks\captchabreak\data\zoneh.org\seg'
        
    count = 0
    zos = ZonehorgClassifier()
    for path in walkdir(datapath):
        imgs = zos._segment(path)
        for i in range(len(imgs)):
            fname = os.path.join(output, 'zone_%d.jpg'%count)
            #cv.ShowImage('d%d'%i, imgs[i])
            #cv.WaitKsImage(fname, imgs[i])
            count += 1
            
def classify_singlechar():
    traindata = r'D:\projects\python\xunworks\captchabreak\data\zoneh.org\rename'
    outdir = r'D:\projects\python\xunworks\captchabreak\data\zoneh.org\classify_char'
    
    toclassify_data = r'D:\projects\python\xunworks\captchabreak\data\zoneh.org\seg'
    
    try:
        os.makedirs(outdir)
    except:
        pass
    
    _segmentor = ZonehorgClassifier()
    _segmentor.train(traindata)
    
    filepaths = []
    for path in walkdir(toclassify_data):
        filepaths.append(path)
    count = 0
    for path in filepaths:
        img = _segmentor.load_image(path)
        label = int(_segmentor.classify(img)[0])
        try:
            os.makedirs(os.path.join(outdir, str(label)))
        except:
            pass
        
        outputfile = os.path.join(outdir, str(label), '%d.jpg'%count)
        cv.SaveImage(outputfile, img)
        count += 1

def classify_captcha():
    traindatadir = r'D:\projects\python\xunworks\captchabreak\data\zoneh.org\rename'
    zoneht = ZonehorgClassifier()
    zoneht.train(traindatadir)
    zoneht.write_modeldata()
    zoneht.load_modeldata()
    
    captchar_dir = r'D:\projects\python\xunworks\captchabreak\data\zoneh.org\test'
    filepaths = []
    for path in walkdir(captchar_dir):    
        filepaths.append(path)
        
    count = 0
    for i in range(len(filepaths)):
        path = filepaths[i]
        ret = zoneht.classify_captcha(path)
        print ret
        img = cv.LoadImage(path)
        cv.ShowImage('c', img)
        cv.WaitKey()
    
def test():
    from urllib2 import urlopen
    url = r'http://www.zone-h.org/captcha2.py'
    fname = 'test_captcha.jpg'
    with open(fname, 'wb') as f:
        f.write(urlopen(url).read())
        
    zoneht = ZonehorgClassifier()
    zoneht.load_modeldata()
    
    ret = zoneht.classify_captcha(fname)
    print ret
    img = cv.LoadImage(fname)
    cv.ShowImage('captcha', img)
    cv.WaitKey()
    
if __name__ == '__main__':
    #_segment_to_char()
    #classify_singlechar()
    #classify_captcha()
    classify_captcha()
    