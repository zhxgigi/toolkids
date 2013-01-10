#!/usr/bin/env python
from preprocess import *
from base import BaseClassifier
from classify import Classifier

class ICBCSegmentor(BaseClassifier):
    def __init__(self):
        self.classes = 27
        self.class_sample_num = 8
        self.sample_size = 15#15*15
        self.model = None
    
    def strip_fangkuang(self, img):
        for rowindex in (0, img.height-1):
            row = cv.GetRow(img, rowindex)
            cv.Set(row, 255.0)
        for colindex in (0, img.width-1):
            col = cv.GetCol(img, colindex)
            cv.Set(col, 255.0)
        return img
    
    def segment(self, filepath):
        src_img = cv.LoadImage(filepath, 0)
        src_img = self.strip_fangkuang(src_img)
        cv.Threshold(src_img, src_img, 100, 255, cv.CV_THRESH_BINARY)
        
        img_chunks = vertical_segment(src_img)
        img_chunks = filter(lambda x : count_pixels(x) > 20, img_chunks)
        
        if len(img_chunks) == 3:
            img_chunks = sorted(img_chunks, key=lambda x : x.width, reverse=True)
            max_chunk = img_chunks.pop(0)#assume 2 chunks cannot seg by hist.
            bf_chunks = vertical_segment_bf(max_chunk)
            img_chunks.extend(bf_chunks)
        elif len(img_chunks) == 2:
            for i in range(len(img_chunks)):
                max_chunk = img_chunks.pop(0)
                bf_chunks = vertical_segment_bf(max_chunk)
                img_chunks.extend(bf_chunks)
    
        return img_chunks
         
    def train(self, file_path):
        classes = self.classes
        class_sample_num = self.class_sample_num
        size = self.sample_size
        train_sample_count = classes*class_sample_num
        
        trainData = cv.CreateMat(train_sample_count, size*size, cv.CV_32FC1)
        trainClasses = cv.CreateMat( train_sample_count, 1, cv.CV_32FC1)
        
        filebase = "%d_%d.jpg"
        for i in range(classes):
            for j in range(class_sample_num):
                sample_path = os.path.join(file_path, filebase % (i, j))
                train_sample_image = cv.LoadImage(sample_path, 0)
                
                train_sample_norm_image = normalization_size(train_sample_image, size, size)
                trainClasses[i*class_sample_num + j, 0] = i
                                
                tmp = cv.CreateImage(( size, size ), cv.IPL_DEPTH_32F, 1 )
                
                #//convert 8 bits image to 32 float image
                cv.ConvertScale(train_sample_norm_image, tmp, 0.0039215, 0)
                
                #data = cv.GetSubRect(tmp, (0,0, size,size))
                #//convert data matrix sizexsize to vecor
                srcdata_row = cv.Reshape(tmp, 0, 1)
                dest_row = cv.GetRow(trainData, i*class_sample_num + j)
                cv.Copy(srcdata_row, dest_row, None)
                
    #// learn classifier
        python_training_data=[]
        for i in xrange(trainData.height):
            row = []
            for j in xrange(trainData.width):
                row.append(trainData[i, j])
            python_training_data.append(row)
        
        python_responses=[]
        for i in xrange(trainClasses.height):
            row = []
            for j in xrange(trainClasses.width):
                row.append(trainClasses[i, j])
            python_responses.append(row)
        
        training_data = np.matrix(python_training_data, dtype=np.float32)
        responses = np.matrix(python_responses, dtype=np.float32)
        
        self.model = cv2.KNearest(training_data, responses, None)
        #self.model = cv2.SVM(training_data, responses)
        
    def classify(self, filepath):
        sample_img = cv.LoadImage(filepath, 0)
        sample_img_feature = tran_feature(sample_img, self.sample_size)
        response = self.model.find_nearest(sample_img_feature, 1, None)
        #response = self.model.predict(sample_img_feature)
        return response
        
def segment_catpcha_to_singlechar():
    captchadir = r'D:\projects\python\captchabreak\data\icbc\icbc1213'
    outputdir =  r'D:\projects\python\captchabreak\data\icbc\icbc1213_output'
    try:
        os.mkdir(outputdir)
    except:
        pass
    
    icbc = ICBCSegmentor()
    count = 0
    for root, dirs, files in os.walk(captchadir):
        for file in files:
            path = os.path.join(root, file)
            imgchunks = icbc.segment(path)
            for img in imgchunks:
                outputfile = os.path.join(outputdir, 'icbc_%d.jpg'%count)
                count += 1
                cv.SaveImage(outputfile, img)

def classify_singlechar():
    singlechardir =  r'D:\projects\python\captchabreak\data\icbc\icbc1213_output'
    outputdir = r'D:\projects\python\captchabreak\data\icbc\icbc_c_output'
    try:
        os.mkdir(outputdir)
    except:
        pass
    
    traindata = r'D:\projects\python\captchabreak\data\icbc\icbcaudit'
    cc = Classifier(traindata, class_sample_num=20, size = 20)
    cc.train()
    count =0
    for subdir in cc.classify_map:
        try:
            os.mkdir(os.path.join(outputdir, subdir))
        except:
            pass
    for root, dirs, files in os.walk(singlechardir):
        for file in files:
            path = os.path.join(root, file)
            img = cv.LoadImage(path, 0)
            response = cc.classify_single_char(img)
            
            outputfile = os.path.join(outputdir, response, 'icbc_%d.jpg'%count)
            cv.SaveImage(outputfile, img)
            count += 1
def test():
    traindata = r'D:\projects\python\xunworks\captchabreak\data\icbc\icbcaudit'
    icbc = ICBCSegmentor()
    fname = r'D:\projects\python\xunworks\captchabreak\data\icbc\icbc1000\icbc_0.jpg'
    images = icbc.segment(fname)
    for i in range(len(images)):
        cv.ShowImage('char:%d'%i, images[i])
    cv.WaitKey()
    
if __name__ == '__main__':
    test()
    