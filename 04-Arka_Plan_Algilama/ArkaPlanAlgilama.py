from imutils import resize
import numpy as np
import cv2 as cv

path    = "./people-walking.mp4"
cap     = cv.VideoCapture(path)

bgsMOG  = cv.createBackgroundSubtractorMOG2()
bgsKNN  = cv.createBackgroundSubtractorKNN()
kernel  = cv.getStructuringElement(cv.MORPH_ELLIPSE,(5,5))

# Randomly select 25% frames
frameNum = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
percent  = int(frameNum * .25)
frameIds = cap.get(cv.CAP_PROP_FRAME_COUNT) * np.random.uniform(size = percent)
frames   = []

print("[?] Estimating background...",end="")
for frameId in frameIds:
    cap.set(cv.CAP_PROP_POS_FRAMES, frameId)
    ret, frame = cap.read()
    frames.append(frame)
bgFrame = np.median(frames, axis=0).astype(dtype=np.uint8)
print("...Done!")

print("[?] Playing the video...")
(W, H)  = bgFrame.shape[:2]
cap.set(cv.CAP_PROP_POS_FRAMES, 0)

while True:
    frameNo   = str(int(cap.get(cv.CAP_PROP_POS_FRAMES)))
    frame     = cap.read()[1]
    if frame is None:
        break

    fgMaskMOG = bgsMOG.apply(frame)
    fgMaskMOG = cv.morphologyEx(fgMaskMOG, cv.MORPH_CLOSE, kernel)
    fgMaskMOG_= cv.bitwise_not(fgMaskMOG)
    
    resMOG1   = cv.bitwise_and(bgFrame, bgFrame, mask = fgMaskMOG)
    resMOG2   = cv.bitwise_and(frame, frame, mask = fgMaskMOG_)
    resMOG    = cv.addWeighted(resMOG1, 1, resMOG2, 1, 0)

    fgMaskKNN = bgsKNN.apply(frame)
    fgMaskKNN = cv.morphologyEx(fgMaskKNN, cv.MORPH_CLOSE, kernel)
    fgMaskKNN_= cv.bitwise_not(fgMaskKNN)
    
    resKNN1   = cv.bitwise_and(bgFrame, bgFrame, mask = fgMaskKNN)
    resKNN2   = cv.bitwise_and(frame, frame, mask = fgMaskKNN_)
    resKNN    = cv.addWeighted(resKNN1, 1, resKNN2, 1, 0)

    fgMasks   = np.hstack((fgMaskMOG, fgMaskKNN))
    fgMasks   = resize(fgMasks, width=H)
    fgMasks   = cv.cvtColor(fgMasks, cv.COLOR_GRAY2BGR)

    results   = np.vstack((resMOG, resKNN))
    results   = resize(results, height=W)
    
    w, h      = (fgMasks.shape[0], results.shape[1])
    blank     = np.zeros((w, h, 3), dtype=np.uint8)
    arg       = cv.resize(bgFrame, (h, w))
    cv.putText(blank, frameNo, (0, 0), cv.FONT_HERSHEY_SIMPLEX, 2 , (0,0,0), 2)
    
    # row1      = np.hstack((fgMasks, blank))
    row1      = np.hstack((fgMasks, arg))
    row2      = np.hstack((frame, results))
    res       = np.vstack((row1, row2))
    cv.imshow('Frame', res)
    
    keyboard = cv.waitKey(30)
    if keyboard == 'q' or keyboard == 27:
        break

cap.release()
cv.destroyAllWindows()
