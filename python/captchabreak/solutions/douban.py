#!/usr/bin/env python
from preprocess import *
import cv2
from classify import Classifier

class DoubanSolution(object):
    def filter_edged_noise_chunk(self, chunks, height, width):
        """some noise chunk is aject with edge."""
        filterd = []
        for chunk in chunks:
            tag = False
            for x, y in chunk:
                if x==0 or y == 0 or x== (height-1) or y==(width-1):
                    tag =True
                if tag:
                    break
            if not tag:
                filterd.append(chunk)
                
        print len(chunks)
        print len(filterd)
        return filterd
    
    def is_edged_chunk(self, chunk, height, width):
        for x, y in chunk:
            if x==0 or y == 0 or x == (height-1) or y ==(width-1):
                return True
        return False
    
    def is_edged_img(self, img):
        for x in range(img.height):
            for y in range(img.width):
                if img[x, y] != 0.0:
                    continue
                if x==0 or y == 0 or x== (img.height-1) or y==(img.width-1):
                    return True
        return False
    
    def shape_filter(self, img, size=15):
        left, top, width, height = find_my_roi(img)
        if width <= size and height <= size:
            return True
        
        return False
    
    def segment(self, path):
        mat = cv.LoadImage(path, 1)
        st = time.time()
        out = denoise_background(mat, 220)
        
        st1 = time.time()
        
        img_chunks_useless, point_chunks= color_filling(out)
        point_chunks = sorted(point_chunks, key=lambda x: len(x), reverse=True)
        st2 = time.time()
        
        seg_images = []
        for chunk in point_chunks:
            if self.is_edged_chunk(chunk, mat.height, mat.width):
                continue
            if len(chunk) > 600:
                for x, y in chunk:
                    out[x, y] = 255
            elif len(chunk) < 50:
                for x, y in chunk:
                    out[x, y] = 255
            
            else: 
                chunk_img = cv.CreateImage(cv.GetSize(mat), 8, 1)
                cv.Set(chunk_img, 255.0)
                for x, y in chunk:
                    chunk_img[x, y] = 0.0
                seg_images.append(chunk_img)
                
        st3 = time.time()
        print st3-st2, st2-st1, st1-st,
        
        #
        image_bin = cv.CreateImage(cv.GetSize(mat), 8, 1)
        cv.CvtColor(mat, image_bin, cv.CV_BGR2GRAY)
        cv.ShowImage('origin', mat)
        cv.ShowImage('denoise', out)
        cv.ShowImage('bin', image_bin)
        cv.WaitKey()
        return seg_images

def main():
    traindata = r'D:\projects\python\captchabreak\data\doubanaudit'
    douban = Classifier(traindata, 5)
    douban.train()
    
    testdata = r'D:\projects\python\captchabreak\data\doubanseg'
    outputdir = r'D:\projects\python\captchabreak\data\doubanoutput'
    count =0
    for subdir in douban.classify_map:
        try:
            os.mkdir(os.path.join(outputdir, subdir))
        except:
            pass
    for root, dirs, files in os.walk(testdata):
        for file in files:
            path = os.path.join(root, file)
            img = cv.LoadImage(path, 0)
            response = douban.classify_single_char(img)
            
            outputfile = os.path.join(outputdir, response, 'douban_%d.jpg'%count)
            cv.SaveImage(outputfile, img)
            count += 1
            
    #for root, dirs, files in os.walk(testdata):
    #    for file in files:
    #        path = os.path.join(root, file)
    #        img = cv.LoadImage(path, 0)
    #        cate = douban.classify_single_char(img)
    #        print cate
    #        cv.ShowImage('dubt', img)
    #        cv.WaitKey()
    
    
def segment():
    datapath = r'D:\projects\python\xunworks\captchabreak\data\douban_captcha\test'
    output = r'D:\projects\python\captchabreak\data\doubanseg'
    douban = DoubanSolution()
    count = 0
    
    for root, dirs, files in os.walk(datapath):
        for file in files:
            path = os.path.join(root, file)
            
            origin_image = cv.LoadImage(path, 1)
            
            #cv.AdaptiveThreshold(img, img, 255.0)
            #cv.Threshold(img, img, 100, 255.0, 0)
            st = time.time()
            #denoise_background(origin_image)
            seg_images = douban.segment(path)
            et = time.time()
            print et-st
            for img in seg_images:
                if douban.shape_filter(img):
                    continue
                outfile = os.path.join(output, 'seg_%d.jpg'%count)
                count += 1
                cv.ShowImage('d%d'%count, img)
                
                img = normalization_size(img, 30,30)
                cv.SaveImage(outfile, img)
            cv.WaitKey()
if __name__ == '__main__':
    segment()