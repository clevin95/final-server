import numpy as np
import argparse
import cv2

sign_directory = "/Users/carterlevin/Desktop/top\ crop.png"

# load the image
image = cv2.imread(sign_directory)
# image = cv2.blur(src,(5,5))
# cv2.imshow("Image", image)
# cv2.waitKey(0)
# find all the 'black' shapes in the image
lower = np.array([0, 0, 130])
upper = np.array([100, 100, 250])
shapeMask = cv2.inRange(image, lower, upper)
# find the contours in the mask
(img, cnts, _) = cv2.findContours(shapeMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


selected = []
for c in cnts:
	x,y,w,h = cv2.boundingRect(c)
	# if w > 20 and h > 20:
	selected.append((x,y,w,h))
	cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)


# print("I found %d black shapes" % (len(cnts)))
# for c in cnts:
# 	# draw the contour and show it
# 	approx = cv2.approxPolyDP(c,0.40*cv2.arcLength(c,True), True)
# 	x,y,w,h = cv2.boundingRect(approx)
# 	cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)

cv2.imshow("Image", image)
cv2.waitKey(0)