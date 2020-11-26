import matplotlib.pyplot as plt
from imutils import resize
import numpy as np
import cv2 as cv

cover      = cv.imread("./maske.png")
bgr_mean   = np.mean(cover, axis=(0,1))
bgr_mean   = np.array(bgr_mean, np.uint8, ndmin=3)
hsv_mean   = cv.cvtColor(bgr_mean, cv.COLOR_BGR2HSV).ravel()

lowerBound = hsv_mean - (15, 75, 75)
upperBound = hsv_mean + (15, 75, 75)

lowerBound[lowerBound <   0] =   0
upperBound[upperBound > 255] = 255

# Dahili kameraları kullanmak için
# video = cv.VideoCapture(0)
# 
# Bilgisayara kayıtlı bir videoyu kullanmak için
# path  = "./1911 - A Trip Through New York City.mp4"
# video = cv.VideoCapture(path)
#
# "IP Camera" Bağlantısı
video = cv.VideoCapture('http://192.168.1.34:8080/video')

print("[?] BACKGROUND IS BEING RECORDED")
for time in range(60):
    ret, canvas = video.read()   
    canvas      = resize(canvas, width=720) 
    if not ret:
        continue
print("[?] ...DONE")

print("[?] READY 2 GO...")
while video.isOpened():
    ret, frame  = video.read()
    frame       = resize(frame, width=720)
    
    if not ret:
        break
    
    hsv    = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    mask   = cv.inRange(hsv, lowerBound, upperBound)
    
    kernel = cv.getStructuringElement(cv.MORPH_CROSS, (3,3))
    mask   = cv.morphologyEx(mask, cv.MORPH_OPEN  , kernel)
    mask   = cv.morphologyEx(mask, cv.MORPH_DILATE, kernel)
    mask_  = cv.bitwise_not(mask)
    
    res_1  = cv.bitwise_and(canvas, canvas, mask = mask ) 
    res_2  = cv.bitwise_and(frame , frame , mask = mask_)
    res    = cv.addWeighted(res_1, 1, res_2, 1, 0)
    
    row    = np.hstack((res_1, res_2))
    row    = resize(row, width=row.shape[1]//2)
    res    = np.vstack((row, res))
    cv.imshow('frame', res)
 
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv.destroyAllWindows()
