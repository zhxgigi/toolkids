#!/usr/bin/env python
import os
import numpy as np
from preprocess import *

class Classifier(object):
    def __init__(self, datadir, class_sample_num=10, size=20, model='knn'):
        self.datadir = datadir
        self.sample_size = size
        self.classify_map = os.listdir(self.datadir)
        self.classes_num = len(self.classify_map)
        self.class_sample_num = class_sample_num
        self.train_sample_count = self.classes_num * self.class_sample_num
        
        self.trainSamples = cv.CreateMat(self.train_sample_count, self.sample_size*self.sample_size, cv.CV_32FC1)
        self.trainClasses = cv.CreateMat(self.train_sample_count, 1, cv.CV_32FC1)
        self.model_type = model
        self.model = None
        
    def tran_feature(self, train_sample_image, retmat=False):
        cv.Threshold(train_sample_image, train_sample_image, 100, 255, cv.CV_THRESH_BINARY)
        train_sample_norm_image = normalization_size(train_sample_image, self.sample_size, self.sample_size)
               
        tmp = cv.CreateImage(( self.sample_size, self.sample_size ), cv.IPL_DEPTH_32F, 1 )
        
        #//convert 8 bits image to 32 float image
        cv.ConvertScale(train_sample_norm_image, tmp, 0.0039215, 0)
        
        #//convert data matrix sizexsize to vecor
        
        responses = cv.Reshape(tmp, 0, 1)
        if retmat:#used by train
            return responses
        else:#used by classify
            feature_list = [responses[0, i] for i in range(responses.width)]
            responses_matrix = np.matrix(feature_list, dtype=np.float32)
            return responses_matrix
    
    def gen_train_samples(self):
        for i in range(self.classes_num):
            cate_path = os.path.join(self.datadir, self.classify_map[i])
            cate_file_names = os.listdir(cate_path)
            for j in range(self.class_sample_num):
                cate_file_path = os.path.join(cate_path, cate_file_names[j])
                
                train_sample_image = cv.LoadImage(cate_file_path, 0)
                feature = self.tran_feature(train_sample_image, retmat=True)
                
                dest_row_id = i*self.class_sample_num + j
                dest_row = cv.GetRow(self.trainSamples, dest_row_id)
                cv.Copy(feature, dest_row, None)
                
                #for i in range(feature.height):
                #    for j in range(feature.width):
                #        print feature[i,j]
                self.trainClasses[dest_row_id, 0] = i
                #print cate_file_path, i, dest_row_id
    
    def train(self):
        self.gen_train_samples()
        
        python_training_data=[]
        for i in xrange(self.trainSamples.height):
            row = []
            for j in xrange(self.trainSamples.width):
                row.append(self.trainSamples[i, j])
            python_training_data.append(row)
        
        python_responses=[]
        for i in xrange(self.trainClasses.height):
            row = []
            for j in xrange(self.trainClasses.width):
                row.append(self.trainClasses[i, j])
            python_responses.append(row)
        
        training_data = np.matrix(python_training_data, dtype=np.float32)
        responses = np.matrix(python_responses, dtype=np.float32)
        
        if self.model_type == 'knn':
            self.model = cv2.KNearest(training_data, responses, None)
        elif self.model_type == 'svm':
            self.model = cv2.SVM(training_data, responses)
    
    def classify_single_char(self, image):
        if not self.model:
            raise Exception("model not train.")
        image_feature = self.tran_feature(image)
        
        if self.model_type == 'knn':
            response = self.model.find_nearest(image_feature, 5, None)[0]
        elif self.model_type == 'svm':
            response = self.model.predict(image_feature)    
            
        return self.classify_map[int(response)]
        #return int(response)
        
def testaccury():
    datadir = r'D:\projects\python\captchabreak\data\icbc\icbcaudit'
    testdata = r'D:\projects\python\captchabreak\data\icbc\icbc_char'
    filebase = "%d_%d.jpg"
    
    cc = Classifier(datadir, class_sample_num=5, size = 20, model='svm')
    cc.train()
    
    #img = cv.LoadImage('icbc_58.jpg', 0)
    #print cc.classify_single_char(img)
    
    right_count = 0.
    wrong_count = 0.
    for class_tag in range(27):
        for j in range(0,10):
            sample_path = os.path.join(testdata, filebase % (class_tag, j))
            img = cv.LoadImage(sample_path, 0)
            
            res = cc.classify_single_char(img)
            print res
            if res == class_tag:
                right_count += 1
            else:
                wrong_count +=1
    total = right_count+wrong_count
    
    print "total: %d, right: %d, wrong %d" % (total, right_count, wrong_count)
    print float(right_count/total)
    
    
if __name__ == '__main__':
    #testaccury()
    
    datadir = r'D:\projects\python\captchabreak\data\icbc\icbcaudit'
    cc = Classifier(datadir, class_sample_num=20, model='knn')
    cc.train()
    
    imagedir = r'D:\projects\python\captchabreak\data\icbc\icbc1213'
    
    from icbc import ICBCSegmentor
    icbc = ICBCSegmentor()
    for root, dirs, files in os.walk(imagedir):
        for file in files:
            path = os.path.join(root, file)
            images = icbc.segment(path)
            
            result = []
            count = 0
            for img in images:
                count += 1
                result.append(cc.classify_single_char(img))
                cv.ShowImage("img%d"%count, img)
            print result
            cv.ShowImage('origin', cv.LoadImage(path, 0))
            cv.WaitKey()
            