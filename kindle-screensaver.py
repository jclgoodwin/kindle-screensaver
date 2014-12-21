#!/usr/bin/python

from ics import Calendar
from urllib2 import urlopen

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

ICAL_URL = 'http://www.york.ac.uk/univ/mis/open/timetablingical/subscribeics.cfm?ref=AC8242C4-0B88-4155-F69D4FD0A8C998E0'

def is_interesting_event(event):
	return 'Careers' not in event.name and 'Reminder' not in event.name and 'Optional Activity' not in event.name

def get_events(url, count):
	cal = Calendar(urlopen(url).read().decode())
	events = cal.events[datetime.now()::'end'] # events that haven't ended
	events = filter(is_interesting_event, events)
	events.sort()
	return events[:count]

def get_image(events):
	image = Image.new('L', (758, 1024), 0)
	draw = ImageDraw.Draw(image)
	fnt = ImageFont.truetype('biolinum.ttf', 36)
	title_fnt = ImageFont.truetype('biolinum.ttf', 48)
	y = 105

	draw.text((45, 30), 'Timetable', font=title_fnt, fill=255)

	for i, event in enumerate(events):
		if event.begin.date() != events[i-1].begin.date(): # first event of the day
			draw.line((40, y-5, 728, y-5), fill=100, width=1) # line
			draw.text((40, y), event.begin.strftime('%a %d %b'), font=fnt, fill=150) # date
		else:
			draw.line((220, y-5, 728, y-5), fill=100, width=1) # line
		draw.text((220, y), event.begin.strftime('%H:%M'), font=fnt, fill=150) # time
		draw.text((320, y), event.name.replace('Computer Science Examination', 'Exam'), font=fnt, fill=255) # name
		y += 40
		if event.location:
			draw.text((320, y), event.location, font=fnt, fill=100) # location
			y += 40	
		y += 15

	return image

events = get_events(ICAL_URL, 14)
image = get_image(events)
image.save('0.png', 'PNG')
