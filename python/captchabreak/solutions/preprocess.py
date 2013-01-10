#!/usr/bin/env python
import cv
import cv2
import array
import os
import time
import numpy as np
import scipy
def _find_point(mat):
    rownum = mat.height
    colnum = mat.width
    
    for x in xrange(rownum):
        for y in xrange(colnum):
            if mat[x, y] != 0.0:
                continue
            #point 2-9
            points_index = []
            points_index = [
                (x-1, y),
                (x-1, y+1),
                (x, y+1),
                (x+1, y+1),
                (x+1, y),
                (x+1, y-1),
                (x, y-1),
                (x-1, y-1)
            ]
            points = array.array('h', [-1, -1])
            
            for px, py in points_index:
                if px >= 0 and px < rownum and py >=0 and py<colnum:
                    points.append(1) if mat[px, py] == 0 else points.append(0)
                else:
                    points.append(0)
            
            a_p1 = 0
            b_p1 = 0
            last = points[-1]
            for pvalue in points[2:]:
                if pvalue == 1:
                    b_p1 += 1;
                if pvalue != last and last == 0:
                    a_p1 += 1;
                last = pvalue
            yield (points, a_p1, b_p1, x, y)

def count_pixels(image):
    count = cv.CountNonZero(image)
    return image.height*image.width-count

def check_point(point, height, width):
    x, y = point
    if x >= 0 and y>=0 and x<height and y<width:
        return True
    return False

def fix_broken(image):
    for i in range(image.height):
        for j in range(image.width):
            if image[i, j] == 0.0:
                continue
            tocheck = ((i-1, j), (i+1, j), (i, j-1), (i, j+1))
            if check_point(tocheck[0], image.height, image.width) and check_point(tocheck[1], image.height, image.width):
                if image[tocheck[0][0], tocheck[0][1]] == 0.0 and image[tocheck[1][0], tocheck[1][1]]==0.0:
                    image[i, j] = 0.0
                    continue
                    
            if check_point(tocheck[2], image.height, image.width) and check_point(tocheck[3], image.height, image.width):
                if image[tocheck[2][0], tocheck[2][1]] == 0.0 and image[tocheck[3][0], tocheck[3][1]]==0.0:
                    image[i, j] = 0.0
            
def find_bone2(mat):
    rownum = mat.height
    colnum = mat.width
    
    counter = 1
    itercount=0
    to_delete = set()
    while (1):
        # subiter2
        for points, a_p1, b_p1, x, y in _find_point(mat):
            cond_c = points[2] * points[4] * points[6]
            cond_d = points[4] * points[6] * points[8]
            if a_p1 == 1 and b_p1 >= 2 and b_p1 <= 6 and cond_c == 0 and cond_d == 0:
                to_delete.add((x, y))
                counter += 1
        
        if len(to_delete) == 0:
            break
        else:
            for x, y in to_delete:
                mat[x, y] = 255.0
            #cv.SaveImage('prs1.jpg', mat)
            to_delete.clear()
            #print "remove %d points in first subinter." % counter
            
        # subiter2
        for points, a_p1, b_p1, x, y in _find_point(mat):
            cond_c = points[2]*points[4]*points[8]
            cond_d = points[2]*points[6]*points[8]
            if a_p1 == 1 and b_p1 >= 2 and b_p1 <= 6 and cond_c == 0 and cond_d== 0:
                to_delete.add((x, y))
                counter += 1

        if len(to_delete) == 0:
            break
        else:
            for x, y in to_delete:
                mat[x, y] = 255.0
            #cv.SaveImage('prs2.jpg', mat)
            #print "remove %d points in second subinter." % counter
        itercount += 1
    print "iter times: %d" % itercount

def vertical_segment_bf(img, parts=4):
    """vertical segment by brutal force."""
    step = 255 * img.height
    hist_data = []
    left, top, width, height = find_my_roi(img)
    
    #for y in xrange(img.width):
    #    col = cv.GetCol(img, y)
    #    hist_data.append((step-cv.Sum(col)[0])/255.0)
    #   
    #minvalue = min(filter(lambda x : x != 0, hist_data))
    #minindex = hist_data.index(minvalue)
    #minindex = img.width/2
    
    ret_images = []
    step = width/parts
    
    for i in range(parts):
        p1 = left + i*step
        p2 = p1 + step
        roi = (p1, top, p2-p1, height)
        cv.SetImageROI(img, roi)
        tmp = cv.CreateImage(cv.GetSize(img), img.depth, img.nChannels)
        cv.Copy(img, tmp)
        ret_images.append(tmp)
        cv.ResetImageROI(img)    
    return ret_images

def vertical_segment(img, hist_threshold=0):
    """vertical segment by brutal force."""
    total = 255 * img.height
    hist_data = []
    for y in xrange(img.width):
        col = cv.GetCol(img, y)
        hist_data.append((total-cv.Sum(col)[0])/255.0)
    
    for i in range(img.width):
        if hist_data[i] < hist_threshold:
            hist_data[i] = 0
    
    left = 0
    right = 0
    flag = 0
    chunks_img = []
    while(left < img.width):
        if (hist_data[left] == 0):
            left += 1
        else:
            right = left
            while(right < img.width and hist_data[right] != 0):
                right += 1
            rect = (left, 0, right-left, img.height)
            #print "left: %d, right: %d, width: %d, height: %d" % rect
            cv.SetImageROI(img, rect)
            img_roi = cv.CreateImage(cv.GetSize(img), img.depth, img.nChannels)
            cv.Copy(img, img_roi, None)
            chunks_img.append(img_roi)
            cv.ResetImageROI(img)
            left = right
    return chunks_img
            
def vertical_hist(img):
    step = 255 * img.height
    hist_data = []
    for y in xrange(img.width):
        col = cv.GetCol(img, y)
        hist_data.append((step-cv.Sum(col)[0])/255.0)
    
    for i in range(len(hist_data)):
        if hist_data[i] != 0:
            left = i
            
    for i in range(len(hist_data)-1, 0, -1):
        if hist_data[i] != 0:
            right = i
    
    #create view.
    out = cv.CreateImage(cv.GetSize(img), 8, 1)
    cv.Copy(img, out, None)
    
    histgram = cv.CreateImage(cv.GetSize(img), 8, 3)
    cv.Zero(histgram)
    for i in xrange(img.width):
        cv.Line(histgram, (i, hist_data[i]), (i, 0), cv.Scalar(0,0,255), 1)
    cv.Flip(histgram, histgram)
    
    return histgram
    
def horizontal_hist(img):
    step = 255 * img.width
    hist_data = []
    for x in xrange(img.height):
        col = cv.GetRow(img, x)
        hist_data.append((step-cv.Sum(col)[0])/255.0)
    
    for i in range(len(hist_data)):
        if hist_data[i] !=0:
            left = i
            
    for i in range(len(hist_data)-1, 0, -1):
        if hist_data[i] !=0:
            right = i
    
    #create view.
    out = cv.CreateImage(cv.GetSize(img), 8, 1)
    cv.Copy(img, out, None)
    
    histgram = cv.CreateImage(cv.GetSize(img), 8, 3)
    cv.Zero(histgram)
    for i in xrange(img.height):
        cv.Line(histgram, (hist_data[i], i), (0, i), cv.Scalar(0,0,255), 1)
    
    return histgram

def color_filling(image, pixels_threshod=0, connnum=4):
    """
    segment image by color filling algorithm.
    """
    img = cv.CreateImage(cv.GetSize(image), image.depth, image.nChannels)
    cv.Copy(image, img)
    img_chunks = []
    
    queue = []
    height = img.height
    width = img.width
    fg_color = 0.0
    flood_color = 255.0
    for i in xrange(img.height):
        for j in xrange(img.width):
            if img[i, j] == fg_color:
                queue.append((i,j))
                chunk = []
                while(len(queue)):
                    point = queue.pop(0)
                
                    img[point] = flood_color
                    chunk.append(point)
                    x, y = point
                    if connnum == 4:
                        points_tocheck = [(x, y-1), (x, y+1), (x-1, y), (x+1, y)]
                    else:
                        points_tocheck = [(x, y-1), (x, y+1), (x-1, y), (x+1, y), (x-1, y-1), (x-1, y+1), (x+1, y-1), (x+1, y+1)]
                    
                    for x, y in points_tocheck:
                        if x >=0 and x <= (height-1) and y >=0 and y <=(width-1) and img[x, y] == fg_color:
                            queue.append((x, y))
                            chunk.append((x, y))
                            img[x, y] = flood_color
                img_chunks.append(chunk)
                
    point_chunks = filter(lambda x : len(x) >=pixels_threshod, img_chunks)
    img_chunks = []
    for points in point_chunks:
        tmpimg = cv.CreateImage(cv.GetSize(image), image.depth, image.nChannels)
        cv.Set(tmpimg, 255.0)
        for x, y in points:
            tmpimg[x, y] = 0.0
        img_chunks.append(tmpimg)
    return (img_chunks, point_chunks)

def euclidean_dist(p1, p2):
    sum = 0.0
    for i in range(len(p1)):
        sum += abs(p1[i]-p2[i])**2
    return sum**(0.5)

st = time.time()
#print dist((0,0,0),(255,255,255)),time.time()-st
#print np.linalg.norm(np.array((0.0, 0.0, 0.0))-np.array((255.0, 255.0, 255.0))), time.time()-st

def denoise_background(img, threshold=100.0):
    height = img.height
    width = img.width
    out = cv.CreateImage(cv.GetSize(img), 8, 1)
    cv.CvtColor(img, out, cv.CV_BGR2GRAY );
    for i in range(height):
        for j in range(width):
            #dist = np.linalg.norm(np.array((0.0, 0.0, 0.0))-np.array((img[i,j])))
            dist = euclidean_dist((0.0,0.0,0.0), img[i,j])
            out[i, j] = 255.0 if dist >= threshold else 0.0
    return out

def filter_by_hsv(img):
    out = cv.CreateImage(cv.GetSize(img), 8, 3)
    #cv.CvtColor(img, out, cv.CV_RGB2HSV);
    for i in range(img.height):
        for j in range(img.width):
            hsv_color = list(img[i,j])
            hsv_color[0] = 100
            hsv_color[1] = 125
            #hsv_color[2o] = 0.0
            out[i,j] = hsv_color
    return out

def find_my_roi(image):
    maxval = image.width * 255.0
    flag = 0
    for i in range(image.height):
        row = cv.GetRow(image, i)
        sum = cv.Sum(row)
        if sum[0] < maxval:
            bottom = i
            if not flag:
                top = i
                flag = 1
    
    maxval = image.height * 255.0
    flag = 0
    for i in range(image.width):
        col = cv.GetCol(image, i)
        sum = cv.Sum(col)
        if sum[0] < maxval:
            right = i
            if not flag:
                left = i
                flag = 1
    
    return left, top, right-left, bottom-top

def normalization_size(image, new_width, new_height):
    left, top, width, height = find_my_roi(image)
    size = width if width > height else height
    
    src_rect = cv.GetSubRect(image, (left, top, width, height))
    
    result = cv.CreateImage((size, size), 8, 1)
    cv.Set(result, 255.0, None)
    
    center_x = (size - width)/2
    center_y = (size - height)/2
    out_rect = cv.GetSubRect(result, (center_x, center_y, width, height))
    cv.Copy(src_rect, out_rect, None)
    
    scaled_img = cv.CreateImage( ( new_width, new_height), 8, 1)
    cv.Resize(result, scaled_img, cv.CV_INTER_NN);
    return scaled_img

def tran_feature(train_sample_image, size, retmat=False):
    train_sample_norm_image = normalization_size(train_sample_image, size, size)
                       
    tmp = cv.CreateImage(( size, size ), cv.IPL_DEPTH_32F, 1 )
    
    #//convert 8 bits image to 32 float image
    cv.ConvertScale(train_sample_norm_image, tmp, 0.0039215, 0)
    data = cv.GetSubRect(tmp, (0,0, size,size))
    #//convert data matrix sizexsize to vecor
    responses = cv.Reshape(data, 0, 1)
    
    if retmat:
        return responses
    else:
        feature_list = [responses[0, i] for i in range(responses.width)]    
        responses_matrix = np.matrix(feature_list, dtype=np.float32)
        return responses_matrix

def detect_circle(im):
    gray = cv.CreateImage(cv.GetSize(im), 8, 1)
    cv.CvtColor(im, gray, cv.CV_BGR2GRAY)
    #cv.Canny(gray, gray, 50, 200, 3)
    #cv.Smooth(gray, gray, cv.CV_GAUSSIAN, 9, 9)
    
    python_training_data = []
    for i in xrange(gray.height):
        row = []
        for j in xrange(gray.width):
            row.append(int(gray[i, j]))
            print gray[i, j]
            
        python_training_data.append(row)
    training_data = np.array(python_training_data)
    circles = cv2.HoughCircles(training_data, cv.CV_HOUGH_GRADIENT, 2, 32);
    for (x, y, radius) in circles:
        print x, y, radius
    #storage = cv.CreateMat(im.width, 1, cv.CV_32FC3)
    #
    #cv.HoughCircles(edges, storage, cv.CV_HOUGH_GRADIENT, 2, gray.height/4, 200, 100)
    ## Now, supposing it found circles, how do I extract the information?
    #print storage

def walkdir(rootdir):
    for root, dirs, files in os.walk(rootdir):
        for file in files:
            yield os.path.join(root, file)
            
def color_filling2(image, pixels_threshod=0, conn=4):
    """find strong connect chunk."""
    img = cv.CreateImage(cv.GetSize(image), image.depth, image.nChannels)
    cv.Copy(image, img)
    img_chunks = []
    
    queue = []
    height = img.height
    width = img.width
    fg_color = 0.0#black, not detect
    detected_color = 13.0
    bg_color = 255.0 #white
    count = 0
    checked = set()
    for i in xrange(img.height):
        for j in xrange(img.width):
            count += 1
            #print count, i, j
            if img[i, j] == fg_color:
                queue.append((i,j))
                chunk = []
                while(len(queue)):
                    point = queue.pop(0)
                    
                    x, y = point
                    #img[x, y] = detected_color # why here is not ok, but in add point.
                    checked.add((x, y))
                    
                    points_tocheck = [(x, y-1), (x, y+1), (x-1, y), (x+1, y), (x-1, y-1), (x-1, y+1), (x+1, y-1), (x+1, y+1)]
                    
                    valid_undetect_neighbors = []
                    valid_neighbors_count = 0
                    
                    for nx, ny in points_tocheck:
                        if nx >=0 and nx <= (height-1) and ny >=0 and ny <= (width-1):
                            if img[nx, ny] != bg_color:
                                valid_neighbors_count += 1

                            if img[nx, ny] == fg_color:
                                valid_undetect_neighbors.append((nx, ny))
                                img[nx, ny] = detected_color
                    #print "x: %d, y: %d, validneighbors: %s" % (x, y, str(valid_undetect_neighbors))                        
                    if valid_neighbors_count >= conn:
                        chunk.append((x, y))#as a point of chunk.
                    
                    for x, y in valid_undetect_neighbors:
                        queue.append((x, y))
                    #print len(queue), len(checked), len(valid_undetect_neighbors)        
                if chunk:
                    #print "detect a chunk, points: %d" % len(chunk)
                    img_chunks.append(chunk)
                
                
    point_chunks = filter(lambda x : len(x) >=pixels_threshod, img_chunks)
    
    ret_imgs = []
    tmpimg = cv.CreateImage(cv.GetSize(image), image.depth, image.nChannels)
    cv.Set(tmpimg, 255.0)
    for points in point_chunks:
        for x, y in points:
            tmpimg[x, y] = 0.0
    return (tmpimg, point_chunks)
    
    
if __name__ == '__main__':
    dir = r'C:\Users\zhanghx\Desktop\captchas\forhist.jpg'
    image = cv.LoadImage(dir, 0)
    cv.Threshold(image, image, 40, 255, cv.CV_THRESH_BINARY)
    #imgs, null = color_filling2(image, 6)
    #cv.ShowImage('image', image)
    #cv.ShowImage('colorfilling2', imgs)
    hist = vertical_hist(image)
    cv.SaveImage(dir+'hist.jpg', hist)
    #cv.WaitKey()