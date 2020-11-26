import cv2 as cv
import numpy as np

# An Improved Median Filtering Algorithm for Image Noise Reduction (Youlian Zhu, Cheng Huang)

def Improved_Median_Filtering(im, k=3):
    canvas       = np.zeros_like(im)
    imH, imW     = im.shape[:2]
    
    def Computation(im):
        med_ = np.median(im)
        min_ = np.min(im)
        max_ = np.max(im)
        A1   = med_ - min_
        A2   = med_ - max_
        return A1, A2

    def Judgment(im):
        A1, A2 = Computation(im)
        if A1 > 0 and A2 < 0:
            return True
        return False
    
    done, k_     = False, k
    for y in range(imH):
        for x in range(imW):
            while not done:
                pad      = (k_ - 1) // 2
                ymin     = max(  0, y-pad)
                ymax     = min(imH, y+pad)
                xmin     = max(  0, x-pad)
                xmax     = min(imW, x+pad)
                roi      = im[ymin:ymax+1,xmin:xmax+1]
                done     = Judgment(roi)
                if not done:
                    k_  += 2
            canvas[y,x] = np.median(roi)
            done, k_    = False, k
    return canvas


# GRAY Image
filename = "./gurultu2.png"
im       = cv.imread(filename, cv.IMREAD_GRAYSCALE)
res_1    = Improved_Median_Filtering(im)
res_1    = np.hstack((im, res_1))

# RGB Image
filename = "./gurultu1.png"
im       = cv.imread(filename)

red      = im[...,2]
red_     = Improved_Median_Filtering(red)

green    = im[...,1]
green_   = Improved_Median_Filtering(green)

blue     = im[...,0]
blue_    = Improved_Median_Filtering(blue)

res_2    = cv.merge([blue_, green_, red_])
res_2    = np.hstack((im, res_2))

cv.imshow("GRAY Image", res_1)
cv.imshow("RGB Image", res_2)
cv.waitKey()
cv.destroyAllWindows()


