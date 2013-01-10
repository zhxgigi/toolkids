#!/usr/bin/env python
import cPickle as pickle
import cv2
import cv
import os
import random
from preprocess import *

class BaseClassifier(object):
    def __init__(self, modeldir):
        self.modeldir = modeldir if modeldir else os.path.join(os.path.dirname(__file__), 'models', self.name)
        
    def segment(self, filepath):
        raise Exception("subclass should overide this func.")
    
    def _load_image(self, path):
        raise Exception("subclass should overide this func.")
    
    def _load_traindata(self, datadir):
        """{cate: [path]}"""
        cate_paths = {}
        for filepath in walkdir(datadir):
            cate = filepath.split(os.sep)[-2]
            
            path_list = cate_paths.get(cate, [])
            path_list.append(filepath)
            cate_paths[cate] = path_list
        
        holders = {}
        for key, values in cate_paths.iteritems():
            random.shuffle(values)
            holders[key] = values[:self.class_sample_num]
        return holders
        
    def classify_captcha(self, filepath):
        imgs = self.segment(filepath)
        result = []
        for img in imgs:
            response = self.classify(img)
            label = int(response[0])
            result.append(chr(label))
        return ''.join(result)
        
    def train(self, filepath):
        """actually transform the filepath files to matrix data here."""
        traindata = self._load_traindata(filepath)
        
        size = self.sample_size
        train_sample_count = len(reduce(lambda x, y : x + y, traindata.values()))
        
        trainData = cv.CreateMat(train_sample_count, size*size, cv.CV_32FC1)
        trainClasses = cv.CreateMat( train_sample_count, 1, cv.CV_32FC1)
        
        step = 0
        for cate, sample_paths in traindata.iteritems():
            for samplepath in sample_paths:
                train_sample_image = self._load_image(samplepath)
                
                train_sample_norm_image = normalization_size(train_sample_image, size, size)
                
                #cv.ShowImage('v', train_sample_norm_image)
                #cv.WaitKey()
                
                trainClasses[step, 0] = int(cate)
                                
                tmp = cv.CreateImage(( size, size ), cv.IPL_DEPTH_32F, 1 )
                
                #//convert 8 bits image to 32 float image
                cv.ConvertScale(train_sample_norm_image, tmp, 0.0039215, 0)
                
                #data = cv.GetSubRect(tmp, (0,0, size,size))
                #//convert data matrix sizexsize to vecor
                srcdata_row = cv.Reshape(tmp, 0, 1)
                dest_row = cv.GetRow(trainData, step)
                cv.Copy(srcdata_row, dest_row, None)
                step += 1
                
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
        
        self._training_data = np.matrix(python_training_data, dtype=np.float32)
        self._responses = np.matrix(python_responses, dtype=np.float32)
        
    def classify(self, sample_img):
        sample_img_feature = tran_feature(sample_img, self.sample_size)
        if self.model_type == 1:
            response = self.model.find_nearest(sample_img_feature, 1, None)
        elif self.model_type == 2:
            lable = self.model.predict(sample_img_feature)
            response = [lable, ]
        else:
            raise "Model Type error, %s" % self.model_type
        return response
    
    def load_modeldata(self):
        with open(os.path.join(self.modeldir, 'traindata.model')) as f:
            self._training_data = pickle.load(f)
        with open(os.path.join(self.modeldir, 'response.model')) as f:
            self._responses = pickle.load(f)
        
        if self.model_type == 1:
            self.model = cv2.KNearest(self._training_data, self._responses, None)
        elif self.model_type == 2:
            self.model = cv2.SVM(self._training_data, self._responses)
        else:
            raise "Model Type error, %s" % self.model_type
    
    def write_modeldata(self):
        try:
            os.makedirs(self.modeldir)
        except:
            pass
        
        with open(os.path.join(self.modeldir, 'traindata.model'), 'wb') as f:
            pickle.dump(self._training_data, f)
        with open(os.path.join(self.modeldir, 'response.model'), 'wb') as f:
            pickle.dump(self._responses, f)
    
