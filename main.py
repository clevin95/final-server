import io
import sys
import os
import numpy as np
import argparse
import cv2
from io import StringIO
import re
from PIL import Image
import calendar

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

days = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"]

def parse_day(day_string):
	return days.index(str(day_string[:3]))

def parse_hour(hour_string):
	if hour_string == "midnight":
		return 0.0
	hours_min = hour_string.split(":")
	hour_str = re.sub("\D", "", hours_min[0])

	try:
		hour = float(hour_str)
		if len(hours_min) > 1:
			minutes = float(hours_min[1])
			hour += (minutes / 60.0)
		if "pm" in hour_string:
			hour += 12
		return hour
	except ValueError:
		return None

def parse_words(full_string):
	print(full_string)
	words = re.split(r'[-\n ]', full_string.lower())
	print(words)
	content = {"positive" : True, "commercial" : False}
	dates = []
	date = None
	and_flag = False
	if "no parking" in full_string or "no standing" in full_string:
		content["positive"] = False
	if "comercial" in full_string:
		content["comercial"] = True
	for word in words:
		if "exc" in word:
			date = {"except" : True}
			dates.append(date)

		if "and" == word or "&" == word:
			and_flag = True

		if "am" in word or "pm" in word or ":" in word or "midnight" in word:
			parsed_hour = parse_hour(word)
			if parsed_hour is None:
				continue
			if date is None:
				date = {}
				dates.append(date)
			if "hours" not in date:
				date["hours"] = [{}]
			elif "begin" in date["hours"][-1] and "end" in date["hours"][-1]:
				date["hours"].append({})
			hour = date["hours"][-1]
			if "begin" not in hour:
				hour["begin"] = parsed_hour
			else:
				hour["end"] = parsed_hour

		elif word[:3] in days:
			parsed_day = parse_day(word)
			if date is None:
				date = {}
				dates.append(date)
			elif "hours" in date and "days" in date:
				if len(date["days"]) > 1:				
					date = {}
					dates.append(date)
			if "days" not in date:
				date["days"] = []

			if len(date["days"]) == 0:
				date["days"] = [parsed_day]
			else:
				if and_flag:
					date["days"].append(parsed_day)
					and_flag = False
				else:
					date["days"] = list(range(date["days"][0], parsed_day + 1))

	content["dates"] = dates
	return content


def main():
	sign_directory = sys.argv[1]
	client = vision.ImageAnnotatorClient()
	file_name = os.path.join(
	    os.path.dirname(__file__),
	    sign_directory)

	# Loads the image into memory
	with io.open(file_name, 'rb') as image_file:
	    content = image_file.read()

	image = types.Image(content=content)
	# Performs label detection on the image file
	response = client.text_detection(image=image)
	labels = response.label_annotations
	full_text = response.full_text_annotation.text
	payload = {}
	signs = []

	signs.append(parse_words(full_text))
	payload["signs"] = signs

	print(payload)
    
if __name__ == "__main__":
	main()



# Convert string times to military time
# def parse_hours(times):
# 	if times[0].lower() == "midnight":
# 		begin = 0
# 	else:
# 		print(times[0])
# 		begin_str = re.sub("\D", "", times[0])
# 		print(begin_str)
# 		begin = float(begin_str)
# 		print(begin)
# 		if begin >= 100:
# 			begin /= 100
# 		if "pm" in times[0].lower():
# 			begin += 12
# 	if times[-1].lower() == "midnight":
# 		end = 0
# 	else:
# 		end_str = re.sub("\D", "", times[-1])
# 		end = float(end_str)
# 		if end >= 100:
# 			end /= 100
# 		if "pm" in times[-1].lower():
# 			end += 12
# 	time = {"begin" : begin, "end" : end}
# 	return time

# Takes in string of days and int array cooresponding to days
# def parse_days(day_string):
# 	words = day_string.split()
# 	start = None
# 	end = None
# 	for word in words:
# 		if word[:3].lower() not in days:
# 			continue
# 		elif start is None:
# 			start = days.index(str(word[:3]).lower())
# 		else:
# 			end = days.index(str(word[:3]).lower())
# 			break

# 	if end is None:
# 		return [start]
# 	else:
# 		return list(range(start, end + 1))

# def parse_string(full_string):
# 	full_string = full_string.lower()
# 	s = StringIO(full_string)
# 	content = {"positive" : True, "commercial" : False}
# 	dates = []
# 	date = None
# 	for line in s:
# 		if "no parking" in line or "no standing" in line:
# 			content["positive"] = False
# 		if "comercial" in line:
# 			content["comercial"] = True
# 		if "except" in line:
# 			date = {"except" : True}
# 			dates.append(date)
# 		for day in days:
# 			if day in line:
# 				if date is None or "days" in date:
# 					date = {}
# 					dates.append(date)
# 				date["days"] = parse_days(line)
# 				break
# 		if "am" in line or "pm" in line:
# 			times = re.findall(r"[\w']+", line)
# 			if len(times) >= 2:
# 				hours = parse_hours(times)
# 				if date is None or "hours" in date:
# 					date = {}
# 					dates.append(date)
# 				date["hours"] = hours

# 	content["dates"] = dates
# 	return content

# i = 0
# for annotation in response.text_annotations:
# 	# print(annotation)
# 	vertices = annotation.bounding_poly.vertices
# 	# print(vertices)
# 	x = vertices[0].x
# 	y = vertices[0].y
# 	r = vertices[1].x
# 	l = vertices[2].y
# 	img = Image.open(file_name)
# 	# print(img.size)
# 	# print(x, y, w, h)
# 	img2 = img.crop((x, y, r, l))
# 	img2.save("im(%d).png" % i)
# 	print(i, img2.palette)
# 	i += 1


# i = 0
# for filename in os.listdir(sign_directory):
# 	filepath = sign_directory + filename
# 	file_name = os.path.join(
# 	    os.path.dirname(__file__),
# 	    filepath)

# 	# Loads the image into memory
# 	with io.open(file_name, 'rb') as image_file:
# 	    content = image_file.read()

# 	image = types.Image(content=content)
# 	response = client.text_detection(image=image)
# 	# labels = response.label_annotations
# 	# annotations = response.full_text_annotation.text
# 	print(file_name)
# 	print(response)
# 	i += 1
# 	if i == 1:
# 		break
