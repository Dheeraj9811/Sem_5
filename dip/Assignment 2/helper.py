import cv2
import random
import numpy as np



#salt and pepper noise function

def salt_pepper_noise(image, prob):
    output_image = np.zeros(image.shape)
    thres = 1 - prob 
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            value = random.random()
            if value < prob:
                output_image[i][j] = 0
            elif value > thres:
                output_image[i][j] = 255
            else:
                output_image[i][j] = image[i][j]
    return output_image


#median filter function for kxk mask size
def median_filter(image, k):
    output_image = np.zeros(image.shape)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            # if kernel is out of image boundary, then copy the pixel value
            if i < k//2 or i > image.shape[0] - k//2 or j < k//2 or j > image.shape[1] - k//2:
                output_image[i][j] = image[i][j]
            # else apply median filter
            else:
                output_image[i][j] = np.median(image[i-k//2:i+k//2+1, j-k//2:j+k//2+1])
    return output_image

# Function to Reducing image size from 256*256 to 64*64
def reduce_image_size(img):
    img = cv2.resize(img, (128, 128), interpolation = cv2.INTER_AREA)
    return img


def nearest_neighbour_interpolation(img, scale):
    # get the shape of the image
    print(img.shape)
    r, c = img.shape[0], img.shape[1]
    # get the shape of the new image
    new_h = int(r * scale)
    new_w = int(c * scale)
    # create the new image here
    
    new_img = np.zeros((new_h, new_w))
    # fill the new image
    for i in range(new_h):
        for j in range(new_w):
            # nearest neighbour from originall i
            x = int(i / scale)
            y = int(j / scale)
            # fill the new image
            new_img[i, j] = img[x, y]
    return new_img



# bilinear_interpolation function implemtation
# theory reffered from https://www.youtube.com/watch?v=UhGEtSdBwIQ
def bilinear_interpolation(img, scale):
    # get the shape of the image
    r, c = img.shape[0], img.shape[1]
    # get the shape of the new image
    new_h = int(r * scale)
    new_w = int(c * scale)
    # create the new image here
    new_img = np.zeros((new_h, new_w))
    # fill the new image
    for i in range(new_h):
        for j in range(new_w):
            
            # get the nearest neighbour from originall position
            x1 = int(i / scale)
            y1 = int(j / scale)
            # get the next neighbour
            x2 = min(x1 + 1, r - 1)
            y2 = min(y1 + 1, c - 1)
            # calculate the weights
            a = (i / scale) - x1
            b = (j / scale) - y1
            # calculate the new value
            new_img[i, j] = int((1 - a) * (1 - b) * img[x1, y1] + a * (1 - b) * img[x2, y1] + (1 - a) * b * img[x1, y2] + a * b * img[x2, y2])
    return new_img

def cubic_interpolation(img, scale):
    '''Bicubic interpolation method to convert small size image to original size image
    Parameters:
    img (numpy.ndarray): Small image
    scale (tuple): resizing image scale
    Returns:
    numpy.ndarray: Resized image
    '''
    r, c = img.shape[0], img.shape[1]
    # get the shape of the new image
    new_h = int(r * scale)
    new_w = int(c * scale)
    # create the new image here
    new_img = np.zeros((new_h, new_w))
    # fill the new image
    for i in range(new_h):
        for j in range(new_w):
            
            # get the nearest neighbour from originall position
            x1 = int(i / scale)
            y1 = int(j / scale)
            # get the next neighbour
            x2 = min(x1 + 1, r - 1)
            y2 = min(y1 + 1, c - 1)
            # calculate the weights
            a = (i / scale) - x1
            b = (j / scale) - y1
            # calculate the new value
            new_img[i, j] = int((1 - a) * (1 - b) * img[x1, y1]**3 \
                    + a * (1 - b) * img[x2, y1]**3 \
                    + (1 - a) * b * img[x1, y2]**3 + \
                    a * b * img[x2, y2])

    # img2 = cv2.resize(img, (new_h, new_w), interpolation = cv2.INTER_CUBIC)
    return new_img

# Linear interpolation from  scratch
def linear_interpolation(img, scale):
    # get the shape of the image
    r, c = img.shape[0], img.shape[1]
    # get the shape of the new image
    new_h = int(r * scale)
    new_w = int(c * scale)
    # create the new image here
    new_img = np.zeros((new_h, new_w))
    new_img_= cv2.resize(img, (new_h, new_w), interpolation = cv2.INTER_LINEAR)
    # fill the new image
    for i in range(new_h):
        for j in range(new_w):
            
            # get the nearest neighbour from originall position
            x1 = int(i / scale)
            y1 = int(j / scale)
            # get the next neighbour
            x2 = min(x1 + 1, r - 1)
            y2 = min(y1 + 1, c - 1)
            # calculate the weights
            a = (i / scale) - x1
            b = (j / scale) - y1
            # calculate the new value using mean
            
            temp = np.sum(img[i-2:i+3,j-2:j+3])//25
            new_img[i, j]= temp

        
    return new_img_

# impliment spline interpolation
def spline_interpolation(img, scale):
    # get the shape of the image
    r, c = img.shape[0], img.shape[1]
    # get the shape of the new image
    new_h = int(r * scale)
    new_w = int(c * scale)
    # create the new image here
    new_img = np.zeros((new_h, new_w))
    new_img_= cv2.resize(img, (new_h, new_w), interpolation = cv2.INTER_LANCZOS4)
    # fill the new image
    for i in range(new_h):
        for j in range(new_w):
           
            # get the nearest neighbour from originall position
            x1 = int(i / scale)
            y1 = int(j / scale)
            # get the next neighbour
            x2 = min(x1 + 1, r - 1)
            y2 = min(y1 + 1, c - 1)
            # calculate the weights
            a = (i / scale) - x1
            b = (j / scale) - y1
            # calculate the new value using mean
            if(i<2 or j<2 or i>new_h-3 or j>new_w-3):
                new_img[i, j] = img[x1, y1]
                
            else:
                temp = np.sum(2*img[i-2:i+3,j-2:j+3]**3)
                new_img[i, j]= temp + 1

            temp = np.sum(img[i-2:i+3,j-2:j+3])//9
            new_img[i, j]= temp

        
    return new_img_


def temp_1(img ):
    r, c = img.shape[0], img.shape[1]
     