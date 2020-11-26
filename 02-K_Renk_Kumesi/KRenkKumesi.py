from imutils import resize
from glob import glob
import numpy as np
import cv2 as cv

def NOTHING(x):
    pass

def KMEANS(im, K, criteria, attempts, flags, bestLabels=None):
    Z               = im.reshape((-1,3))
    Z               = np.float32(Z)
    label, center   = cv.kmeans(Z, K, bestLabels, criteria, attempts, flags)[1:]
    
    center          = np.uint8(center)
    result          = center[label.flatten()]
    result          = result.reshape((im.shape))
    return result

IMG_PATHS   = glob("./resimler/*")
print(IMG_PATHS)
WINNAME     = "KMEANS"
cv.namedWindow(WINNAME)

# <<nclusters>> - Number of clusters required at end
cv.createTrackbar('N_CLUSTERS',WINNAME,0,10,NOTHING)
# <<criteria>> = (type, max_iter, epsilon)
# <<type>> of termination criteria. It has 3 flags as below
# 1 - cv.TERM_CRITERIA_MAX_ITER - stop the algorithm after the specified number of iterations, max_iter.
# 2 - cv.TERM_CRITERIA_EPS - stop the algorithm iteration if specified accuracy, epsilon, is reached.
# 3 - cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER - stop the iteration when any of the above condition is met.
cv.createTrackbar('TYPE',WINNAME,0,2,NOTHING)
# <<max_iter>> - An integer specifying maximum number of iterations
cv.createTrackbar('MAX_ITER',WINNAME,0,9,NOTHING)
# <<epsilon>> - Required accuracy
cv.createTrackbar('EPSILON',WINNAME,0,100,NOTHING)
# <<flags>> This flag is used to specify how initial centers are taken. Normally two flags are used for this
# 0 - cv.KMEANS_RANDOM_CENTERS
# 2 - cv.KMEANS_PP_CENTERS
cv.createTrackbar('FLAGS',WINNAME,1,1,NOTHING)
# <<im_index>> This value is used to select a path from paths list
cv.createTrackbar('INDX',WINNAME,1,len(IMG_PATHS)-1,NOTHING)

while True:
    N_CLUSTERS      = cv.getTrackbarPos('N_CLUSTERS',WINNAME)
    INDX            = cv.getTrackbarPos('INDX',WINNAME)
    IMG             = cv.imread(IMG_PATHS[INDX])
    IMG             = cv.resize(IMG, (720, 480))
    if N_CLUSTERS > 1:
        TYPE        = cv.getTrackbarPos('TYPE',WINNAME) + 1
        MAX_ITER    = cv.getTrackbarPos('MAX_ITER',WINNAME) + 1
        EPSILON     = cv.getTrackbarPos('EPSILON',WINNAME) / 100 + 0.01
        CRITERIA    = (TYPE, MAX_ITER, EPSILON)
        
        FLAGS       = cv.getTrackbarPos('FLAGS',WINNAME) * 2
        TEMP        = KMEANS(IMG, N_CLUSTERS, CRITERIA, 10, FLAGS, bestLabels=None)
        print(f"KMEANS(IMG, {N_CLUSTERS}, {CRITERIA}, 10, {FLAGS})")
    else:
        TEMP        = IMG.copy()
    cv.imshow(WINNAME, TEMP)
    
    if cv.waitKey(25) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()
