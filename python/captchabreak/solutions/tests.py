#!/usr/bin/env python
import unittest
from preprocess import *
from icbc import ICBCSegmentor

class ICBCTest(unittest.TestCase):
    def testAcurrty(self):
        icbc = ICBCSegmentor()
        path = r'D:\projects\python\captchabreak\data\icbc_char\output'
        icbc.train(path)
        
        testdata = r'D:\projects\python\captchabreak\data\icbc_char\output'
        filebase = "%d_%d.jpg"
        
        right_count = 0.
        wrong_count = 0.
        for class_tag in range(27):
            for j in range(10, 15):
                sample_path = os.path.join(testdata, filebase % (class_tag, j))
                res = icbc.classify(sample_path)
                if res[0] == class_tag:
                    right_count += 1
                else:
                    wrong_count +=1
        total = right_count+wrong_count
        
        print "total: %d, right: %d, wrong %d" % (total, right_count, wrong_count)
        print float(right_count/total)
    
    def stestMainLoop(self):
        icbc = ICBCSolution()
        class_sample_num = r'D:\projects\python\captchabreak\data\icbc_char\output'
        icbc.train(class_sample_num)
        
        #segment origin
        icbc_data = r'D:\projects\python\captchabreak\data\icbc\icbc'
        count = 0
        output = r'.\tmp\icbcoutput'
        
        from collections import defaultdict
        part_dict = defaultdict(int)
        for fileindex in range(500):
            filepath = os.path.join(icbc_data, 'icbc_%d.jpg' % fileindex)
            img_chunks = icbc.segment_captcha(filepath)
            #print len(img_chunks)
            part_dict[len(img_chunks)] += 1
            
            for img in img_chunks:
                output_file = os.path.join(output, "icbchar_%d.jpg" % count)
                #img = normalization_size(img, 30,30)
                cv.SaveImage(output_file, img)
                count += 1
        print part_dict
        
        #classify previous segment
        to_classify_dir = output
        classify_output_dir = r'.\tmp\icbc_classify'
        
        count = 0
        for root, dirs, files in os.walk(to_classify_dir):
            for file in files:
                fullpath = os.path.join(root, file)
                label = str(icbc.classify(fullpath)[0])[:-2]
                target_dir = os.path.join(classify_output_dir, label)
                if not os.access(target_dir, os.F_OK):
                    os.makedirs(target_dir)
                output_file = os.path.join(target_dir, "%s_%d.jpg"%(label, count))
                img = cv.LoadImage(fullpath)
                cv.SaveImage(output_file, img)
                count += 1
        
    
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
    
    from zonehorg import ZonehorgTrainner
    zz = ZonehorgTrainner()
    zz.load_modeldata()
    