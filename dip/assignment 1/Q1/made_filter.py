# import cv2
import numpy as np

def mean_filter(img , k):
    m, n = img.shape
    if(k == 3):

        mask = np.ones([3, 3], dtype = int)
        mask = mask / 9
        # making new image for mean filer output
        # zero padding output image
        # padding is used to keep the size of image same as the out put image
        new_img = np.zeros([m, n])
        for i in range(1, m-1):
            for j in range(1, n-1):
                temp = img[i-1, j-1]*mask[0, 0]+img[i-1, j]*mask[0, 1]+img[i-1, j + 1]*mask[0, 2]+img[i, j-1]*mask[1, 0]+ img[i, j]*mask[1, 1]+img[i, j + 1]*mask[1, 2]+img[i + 1, j-1]*mask[2, 0]+img[i + 1, j]*mask[2, 1]+img[i + 1, j + 1]*mask[2, 2]
                new_img[i, j]= temp

        return new_img

    if(k==5):
        
        # making new image for mean filer output
        # zero padding output image
        # padding is used to keep the size of image same as the out put image
        new_img = np.zeros([m, n])
        for i in range(2, m-2):
            for j in range(2, n-2):
                temp = np.sum(img[i-2:i+3,j-2:j+3])//25
                new_img[i, j]= temp

        return new_img


def median_filter(img , k):
    m, n = img.shape
    if(k == 3):

        mask = np.ones([3, 3], dtype = int)
        mask = mask / 9
        # making new image for mean filer output
        # zero padding output image
        # padding is used to keep the size of image same as the out put image
        new_img = np.zeros([m, n])
        for i in range(1, m-1):
            for j in range(1, n-1):
                temp = np.median(img[i-1:i+2,j-1:j+2])
                new_img[i, j]= temp

        return new_img

    if(k==5):
        
        # making new image for mean filer output
        # zero padding output image
        # padding is used to keep the size of image same as the out put image
        new_img = np.zeros([m, n])
        for i in range(2, m-2):
            for j in range(2, n-2):
                temp = np.median(img[i-2:i+3,j-2:j+3])
                new_img[i, j]= temp

        return new_img

def roberts_filter(img,direction):
    m,n = img.shape
    if(direction==0):        
        new_img = np.zeros([m, n])
        for i in range(1,m-1):
            for j in range(1,n-1):
                temp = img[i-1,j-1]*(-1) + img[i,j]*1
                new_img[i,j] = temp
        return new_img
    elif(direction==1):
            new_img = np.zeros([m, n])
            for i in range(1,m-1):
                for j in range(1,n-1):
                    temp = img[i-1,j-1]*(1) + img[i,j]*(-1)
                    new_img[i,j] = temp
            return new_img


def Sobel_filter(img , direction ):
    # direction = 0 means x direction, else y direction 
    filter = np.array([[-1,-2,1],[0,0,0],[1,2,1]],ndmin=3)
    m,n = img.shape
    if(direction == 0):
        new_img = np.zeros([m, n])
        for i in range(1,m-1):
            for j in range(1,n-1):
                temp = img[i-1:i+2,j-1:j+2]
                # print(temp)
                temp = np.multiply(temp,filter)
                # print(temp)
                temp = np.sum(temp)
                new_img[i,j] = temp
        return new_img
    else:
        new_img = np.zeros([m, n])
        filter = filter.T
        for i in range(1,m-1):
            for j in range(1,n-1):
                temp = img[i-1:i+2,j-1:j+2]
                # print(temp)
                temp = np.multiply(temp,filter)
                # print(temp)
                temp = np.sum(temp)
                new_img[i,j] = temp
        return new_img

def prewitted_filter(img , direction ):
    # direction = 0 means x direction, else y direction 
    filter = np.array([[-1,0,1],[-1,0,1],[-1,0,1]],ndmin=3)
    m,n = img.shape
    if(direction == 0):
        new_img = np.zeros([m, n])
        for i in range(1,m-1):
            for j in range(1,n-1):
                temp = img[i-1:i+2,j-1:j+2]
                # print(temp)
                temp = np.multiply(temp,filter)
                # print(temp)
                temp = np.sum(temp)
                new_img[i,j] = temp
        return new_img
    else:
        new_img = np.zeros([m, n])
        filter = filter.T
        for i in range(1,m-1):
            for j in range(1,n-1):
                temp = img[i-1:i+2,j-1:j+2]
                # print(temp)
                temp = np.multiply(temp,filter)
                # print(temp)
                temp = np.sum(temp)
                new_img[i,j] = temp
        return new_img

# filter = np.array([[1,1,1],[1,8,1],[1,1,1]],ndmin=3)
def enhen_laplacian_filter(img , direction):
   
    m,n = img.shape
    if(direction == 0):
        filter = np.array([[-1,-1,-1],[-1,8,-1],[-1,-1,-1]],ndmin=3)
        new_img = np.zeros([m, n])
        for i in range(1,m-1):
            for j in range(1,n-1):
                temp = img[i-1:i+2,j-1:j+2]
                    # print(temp)
                temp = np.multiply(temp,filter)
                    # print(temp)
                temp = np.sum(temp)
                new_img[i,j] = temp
        return new_img
    
    elif(direction == 1):
        filter = np.array([[1,1,1],[1,-8,1],[1,1,1]],ndmin=3)
        new_img = np.zeros([m, n])
        for i in range(1,m-1):
            for j in range(1,n-1):
                temp = img[i-1:i+2,j-1:j+2]
                    # print(temp)
                temp = np.multiply(temp,filter)
                    # print(temp)
                temp = np.sum(temp)
                new_img[i,j] = temp
        return new_img


def laplacian_filter(img , direction):
   
    m,n = img.shape
    if(direction == 0):
        filter = np.array([[0,-1,0],[-1,4,-1],[0,-1,0]],ndmin=3)
        new_img = np.zeros([m, n])
        for i in range(1,m-1):
            for j in range(1,n-1):
                temp = img[i-1:i+2,j-1:j+2]
                    # print(temp)
                temp = np.multiply(temp,filter)
                    # print(temp)
                temp = np.sum(temp)
                new_img[i,j] = temp
        return new_img
    
    elif(direction == 1):
        filter = np.array([[0,1,0],[1,-4,1],[0,1,0]],ndmin=3)
        new_img = np.zeros([m, n])
        for i in range(1,m-1):
            for j in range(1,n-1):
                temp = img[i-1:i+2,j-1:j+2]
                    # print(temp)
                temp = np.multiply(temp,filter)
                    # print(temp)
                temp = np.sum(temp)
                new_img[i,j] = temp
        return new_img


def highboost_unsharp_tec(img , k,constant):
    
    filtermask = np.subtract(img,mean_filter(img , k))
    # when k >1 it is know as  unsharp masking 
    new_img = img + constant*filtermask
    return new_img


def scharr(img , direction):
    filter = np.array([[3,0,-3],[10,0,-10],[3,0,-3]],ndmin=3)
    m,n = img.shape
    
    if(direction == 0):
        
        new_img = np.zeros([m, n])
        for i in range(1,m-1):
            for j in range(1,n-1):
                temp = img[i-1:i+2,j-1:j+2]
                    # print(temp)
                temp = np.multiply(temp,filter)
                    # print(temp)
                temp = np.sum(temp)
                new_img[i,j] = temp
        return new_img
    
    elif(direction == 1):
        filter = filter.T
        new_img = np.zeros([m, n])
        for i in range(1,m-1):
            for j in range(1,n-1):
                temp = img[i-1:i+2,j-1:j+2]
                    # print(temp)
                temp = np.multiply(temp,filter)
                    # print(temp)
                temp = np.sum(temp)
                new_img[i,j] = temp
        return new_img

