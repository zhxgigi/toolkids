#!/usr/bin/env python
import unittest
import os
import cv

class CapBreakTest(unittest.TestCase):
    def dtestZonehorg(self):
        from capbreak.zonehorg import ZonehorgClassifier

        zoneht = ZonehorgClassifier()
        zoneht.load_modeldata()
        
        captchar_dir = r'D:\projects\python\xunworks\captchabreak\data\zoneh.org\test'
        filepaths = []
        for root, dirs, files in os.walk(captchar_dir):
            for file in files:
                path = os.path.join(root, file)
                filepaths.append(path)
            
        count = 0
        for i in range(len(filepaths)):
            path = filepaths[i]
            ret = zoneht.classify_captcha(path)
            print ret
            img = cv.LoadImage(path)
            cv.ShowImage('c', img)
            cv.WaitKey()
        
    def testZonehcn(self):
        from capbreak.zoneh import ZonehcnClassifier
        zoneht = ZonehcnClassifier()
        zoneht.load_modeldata()
    
        captchar_dir = r'D:\mytemp\tt'
        filepaths = []
        for root, dirs, files in os.walk(captchar_dir):
            for file in files:
                path = os.path.join(root, file)
                filepaths.append(path)
        count = 0
        for i in range(len(filepaths)):
            path = filepaths[i]
            ret = zoneht.classify_captcha(path)
            print ret
            img = cv.LoadImage(path)
            cv.ShowImage('c', img)
            cv.WaitKey()
    
def profile():
    def test():
        #path = r'D:\projects\python\captchabreak\taobaopay-prs\taobao_5.jpg.png'
        path = 'Captcha.jpg'
        mat = cv.LoadImage(path, 0)
        image_out = cv.CreateImage(cv.GetSize(mat), mat.depth, mat.nChannels);
            
        #cv.Erode(mat, image_out, None, 1);
        cv.Threshold(mat, image_out, 200, 255, cv.THRESH_BINARY)
    
    
        cv.ShowImage('bone', image_out)
        cv.WaitKey()
        find_bone2(image_out)
        cv.ShowImage('origin', mat)
        cv.ShowImage('bone', image_out)
        cv.WaitKey()
    test()   
    #import profile
    #profile.run("test()", "prof.txt")
    #import pstats
    #p = pstats.Stats("prof.txt")
    #p.sort_stats("time").print_stats()
    
if __name__ == '__main__':
    unittest.main()