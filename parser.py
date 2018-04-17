import io
import sys
import os
import re

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


def parse_image(all_signs):
	client = vision.ImageAnnotatorClient()
	signs = []

	for sign_name in all_signs:
		name = "cropped/" + sign_name
		path = os.path.join(
		    os.path.dirname(__file__),
		    name)

		# Loads the image into memory
		with io.open(path, 'rb') as image_file:
		    content = image_file.read()

		image = types.Image(content=content)
		# Performs label detection on the image file
		response = client.text_detection(image=image)
		labels = response.label_annotations
		full_text = response.full_text_annotation.text
		payload = {}

		signs.append(parse_words(full_text))

	return signs

