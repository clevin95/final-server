import numpy as np
import argparse
import cv2
import os
import sys

def find_if_close(cnt1,cnt2):
    row1,row2 = cnt1.shape[0],cnt2.shape[0]
    for i in range(row1):
        for j in range(row2):
            dist = np.linalg.norm(cnt1[i]-cnt2[j])
            if abs(dist) < 10 :
                return True
            elif i==row1-1 and j==row2-1:
                return False


def merge_contours(contours):
	LENGTH = len(contours)
	status = np.zeros((LENGTH,1))

	for i,cnt1 in enumerate(contours):
	    x = i    
	    if i != LENGTH-1:
	        for j,cnt2 in enumerate(contours[i+1:]):
	            x = x+1
	            dist = find_if_close(cnt1,cnt2)
	            if dist == True:
	                val = min(status[i],status[x])
	                status[x] = status[i] = val
	            else:
	                if status[x]==status[i]:
	                    status[x] = i+1

	unified = []

	maximum = int(status.max())+1
	for i in range(maximum):
	    pos = np.where(status==i)[0]
	    if pos.size != 0:
	        cont = np.vstack(contours[i] for i in pos)
	        hull = cv2.convexHull(cont)
	        unified.append(hull)
	# cv2.drawContours(image,unified,-1,(0,255,0),2)
	# cv2.imshow("test", image)
	return unified


def get_rects(image, lower_bound, upper_bound):
	shapeMask = cv2.inRange(image, lower_bound, upper_bound)
	# find the contours in the mask
	(img, cnts, _) = cv2.findContours(shapeMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	if len(cnts) == 0:
		return []
	unified = merge_contours(cnts)
	selected = []
	signs = []
	for c in unified:
		x,y,w,h = cv2.boundingRect(c)
		# TO DO: Make the threshold smarter
		if w > 80 and h > 80:
			signs.append((x,y,w,h))
			# cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
	return signs

def crop_rects(image, rects):
	image_files = []
	for i in range(len(rects)):
		(x,y,w,h) = rects[i]
		cropped = image[y: y+h, x:x+w]
		name = str([x,y,w,h]) + ".jpg"
		path = os.path.join("./cropped/" , name)
		# cv2.imshow(name, cropped)
		cv2.imwrite(path, cropped)
		image_files.append(name)
	return image_files

# returns cropped image of each sign
def signs_from_image(sign_directory):
	# load the image
	image = cv2.imread(sign_directory)
	# find all the 'red' shapes in the image
	red_lower = np.array([0, 0, 130])
	red_upper = np.array([100, 100, 250])

	# find all the 'green' shapes in the image
	green_lower = np.array([20, 30, 0])
	green_upper = np.array([55, 80, 10])

	red_signs = get_rects(image, red_lower, red_upper)
	green_signs = get_rects(image, green_lower, green_upper)

	cropped_signs = {}
	cropped_signs["red"] = crop_rects(image, red_signs)
	cropped_signs["green"] = crop_rects(image, green_signs)
	return cropped_signs


# sign_directory = sys.argv[1]
# signs_from_image(sign_directory)