#!/usr/bin/env python
from preprocess import *

class TaobaoSolution(object):
    def __init__(self):
        self.model = None
        self.cate_index = None
        
    def segment(self, filepath):
        image = cv.LoadImage(filepath, 0)
                
        #cv.AdaptiveThreshold(image, image, 255.0)
        cv.Threshold(image, image, 110, 255, 0)
        #cv.Dilate(image,image)
        #image_chunks = vertical_segment_bf(image)
        ret_images = []
        image_chunks, point_chunks = color_filling(image)
        image_chunks = filter(lambda x : count_pixels(x) > 30, image_chunks)
        image_chunks = sorted(image_chunks, key=lambda x: find_my_roi(x)[2], reverse=True)
        image_chunks_len = len(image_chunks)
        #print image_chunks_len
        if image_chunks_len == 1:
            chunks = vertical_segment_bf(image, 4)
            ret_images.extend(chunks)
        elif image_chunks_len == 2:
            pixels_count = map(find_my_roi, image_chunks)
            pixels_times = max(pixels_count[0][2], pixels_count[1][2])/min(pixels_count[0][2], pixels_count[1][2])
            if pixels_times == 1:
                for subimg in image_chunks:
                    ret_images.extend(vertical_segment_bf(subimg, 2))
            else:#2,3,4...
                seg_parts = [3, 1]
                maximg = image_chunks.pop(0)
                ret_images.extend(vertical_segment_bf(maximg, 3))
                ret_images.extend(image_chunks)
        elif image_chunks_len == 3:
            ret_images.extend(image_chunks[:3])
            maximage = ret_images.pop(0)
            ret_images.extend(vertical_segment_bf(maximage, 2))
        else:
            ret_images.extend(image_chunks)
        return ret_images, image
    
    def train(self, datapath):
        classes = 22
        class_sample_num = 5
        train_sample_count = class_sample_num*classes
        sample_size = 15
        trainData = cv.CreateMat(train_sample_count, sample_size*sample_size, cv.CV_32FC1)
        trainClasses = cv.CreateMat(train_sample_count, 1, cv.CV_32FC1)
        
        #for cid in range(classes):
        #    for snum in range(class_sample_num):
        #        sample_file = os.path.join(datapath, '%d_%d.jpg'%(cid, snum))
        classes_name = os.listdir(datapath)
        self.cate_index = classes_name
        for cid in range(classes):
            for snum in range(class_sample_num):
                sample_file = os.path.join(datapath, classes_name[cid], "%s_%d.jpg"%(classes_name[cid], snum))
                sample_file_img = cv.LoadImage(sample_file, 0)
                sample_feature = tran_feature(sample_file_img, sample_size, True)
                dest_row = cv.GetRow(trainData, cid*class_sample_num + snum)
                trainClasses[cid*class_sample_num + snum, 0] = cid
                cv.Copy(sample_feature, dest_row, None)
          
            
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
        
        self.model = cv2.SVM(training_data, responses)
        #self.model = cv2.KNearest(training_data, responses, None)
                
    def classify(self, filepath=None, sample_img=None):
        if not sample_img:
            sample_img = cv.LoadImage(filepath, 0)

        sample_img_feature = tran_feature(sample_img, 15)
        response = self.model.predict(sample_img_feature)
        #response = self.model.find_nearest(sample_img_feature, 10, None)[0]
        return response

def segmentation():
    datapath = r'D:\projects\python\captchabreak\data\taobaopay'
    taobao = TaobaoSolution()
    for root, dirs, files in os.walk(datapath):
        for file in files:
            filepath = os.path.join(root, file)
            image = cv.LoadImage(filepath, 0)
            cv.AdaptiveThreshold(image, image, 255.0)
            cv.Smooth(image, image)
            vhist = vertical_hist(image)
            hhist = horizontal_hist(image)
            
            cv.ShowImage("test", image)
            
            cv.ShowImage("vhist", vhist)
            cv.ShowImage("hhist", hhist)
            
            cv.WaitKey()
            
def classification():
    taobao = TaobaoSolution()
    train_data = r'D:\projects\python\captchabreak\output'
    taobao.train(train_data)

    #classify previous segment
    to_classify_dir = r'D:\projects\python\captchabreak\solutions\tmp\taobaoseg'
    classify_output_dir = r'D:\projects\python\captchabreak\taotaooutput'
    
    count = 0
    for root, dirs, files in os.walk(to_classify_dir):
        for file in files:
            fullpath = os.path.join(root, file)
            label = str(taobao.classify(fullpath))[:-2]
            target_dir = os.path.join(classify_output_dir, label)
            if not os.access(target_dir, os.F_OK):
                os.makedirs(target_dir)
            output_file = os.path.join(target_dir, "%s_%d.jpg"%(label, count))
            img = cv.LoadImage(fullpath)
            cv.SaveImage(output_file, img)
            count += 1

def orc():
    taobao = TaobaoSolution()
    train_data = r'D:\projects\python\captchabreak\output'
    taobao.train(train_data)
    to_classify_dir=r"D:\projects\python\captchabreak\data\taobaopay"
    
    for root, dirs, files in os.walk(to_classify_dir):
        for file in files:
            fullpath = os.path.join(root, file)
            ret_images, image = taobao.segment(fullpath)
            chars = []
            count = 0
            for img in ret_images:
                orc_index = int(taobao.classify(sample_img=img))
                chars.append(taobao.cate_index[orc_index])
                cv.ShowImage("src%d"%count, img)
                count += 1
            print chars
            cv.ShowImage("src", image)
            cv.WaitKey()
            
if __name__ == '__main__':
    file = 'taobao_487.jpg'
    data = r'D:\Projects\pythonworkset\captchabreak\data\taobao1209\taobao'
    taobao = TaobaoSolution()
    for root, dirs, files in os.walk(data):
        for file in files:
            fullpath = os.path.join(root, file)
            #image = cv.LoadImage(fullpath, 0)
            #image_bold = cv.CreateImage(cv.GetSize(image), image.depth, image.nChannels)
            #cv.AdaptiveThreshold(image, image_bold, 255.0)
            
            #fix_broken(image_bold)
            #image_bold = fix_
            #img_chunks, point_chunks = color_filling(image_bold, connnum=4)
            img_chunks, origin_img = taobao.segment(fullpath)
            cnt = 0
            for img in img_chunks:
                cv.ShowImage('taobaoblod%d'%cnt, img)
                cnt+=1
            cv.ShowImage('taobaoblod.jpg', origin_img)
            cv.SaveImage('taobaoblod.jpg', origin_img)
            cv.WaitKey()
    #vhist = vertical_hist(image)
    #find_bone2(image_bold)
    
    #cv.ShowImage('taobaohist.jpg', vhist)
    #
    #
    
    #cv.SaveImage('taobaohist.jpg', vhist)
    
    