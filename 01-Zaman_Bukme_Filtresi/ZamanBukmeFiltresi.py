import cv2 as cv
import numpy as np
IPCAM 			= ...
VIDEO       	= cv.VideoCapture(IPCAM)
ONLINE, FRAME 	= VIDEO.read()
if ONLINE:
	imW   		= int(VIDEO.get(cv.CAP_PROP_FRAME_WIDTH))
	imH   		= int(VIDEO.get(cv.CAP_PROP_FRAME_HEIGHT))
	FPS   		= int(VIDEO.get(cv.CAP_PROP_FPS))
	ONESECOND   	= 1000
	WAIT        	= int(ONESECOND/FPS)

	COLOR, INDX 	= (0, 55,255), 0
	CANVAS, THICC 	= np.zeros_like(FRAME), 3
while True:
	ONLINE, FRAME = VIDEO.read()
	if INDX < imW:
		CANVAS[:,INDX,:] = FRAME[:,INDX,:]
		cv.line(FRAME, (INDX, 0), (INDX, imH), COLOR, thickness=THICC)
		INDX += 1
	cv.imshow("SONUC", np.hstack((FRAME, CANVAS)))
	#if cv.waitKey(WAIT) & 0xFF == ord('q'):
	if cv.waitKey(1) & 0xFF == ord('q'):
		break
	elif cv.waitKey(1) & 0xFF == ord('r'):
		INDX = 0
	if INDX == imW:
		cv.imwrite("deneme.jpg", CANVAS)
		INDX += 1
	print(INDX)
if VIDEO is not None: VIDEO.release()
cv.destroyAllWindows()
