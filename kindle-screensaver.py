#!/usr/bin/python

from ics import Calendar
from urllib2 import urlopen

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

ICAL_URL = "http://www.york.ac.uk/univ/mis/open/timetablingical/subscribeics.cfm?ref=AC8242C4-0B88-4155-F69D4FD0A8C998E0"

def is_interesting_event(event):
	return "Careers" not in event.name and "Reminder" not in event.name and "Optional Activity" not in event.name

def get_events(url, count):
	cal = Calendar(urlopen(url).read().decode())
	events = cal.events[datetime.now()::'end'] # events that haven't ended
	events = filter(is_interesting_event, events)
	events.sort()
	return events[:count]

def image(backdrop_path, events):
	overlay = Image.open(backdrop_path).point(lambda p: p * 0.2)
	draw = ImageDraw.Draw(overlay)
	fnt = ImageFont.truetype('biolinum.ttf', 36)
	title_fnt = ImageFont.truetype('biolinum.ttf', 48)
	white = 255
	black = 0
	y = 105
	draw.text((45, 30), "Timetable", font=title_fnt, fill=white)
	for i, event in enumerate(events):
		if event.begin.date() != events[i-1].begin.date():
			draw.text((40, y), event.begin.strftime("%a %d %b"), font=fnt, fill=white) # date
			draw.line((40, y-5, 728, y-5), fill=black, width=1) # line
		else:
			draw.line((220, y-5, 728, y-5), fill=black, width=1) # line
		draw.text((220, y), event.begin.strftime("%H:%M"), font=fnt, fill=white) # time
		draw.text((320, y), event.name.replace("Computer Science Examination", "Exam"), font=fnt, fill=white) # name
		y += 40
		if event.location:
			draw.text((320, y), event.location, font=fnt, fill=white) # location
			y += 40	
		y += 15
	return overlay

events = get_events(ICAL_URL, 14)

for i in (1, 2, 3, 4, 5, 6, 7, 8):
	image("backdrops/" + str(i) + ".png", events).save(str(i) + ".png", "PNG")
