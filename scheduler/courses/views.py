import requests
import lxml
from lxml import html
from courses.models import Department, Course, Lab
import xml.etree.ElementTree as ET
from django.http import HttpResponse

FALL_URL = "https://secure.upei.ca/cls/dropbox/FallTime.html"
SPRING_URL = "https://secure.upei.ca/cls/dropbox/SpringTime.html"

def scrape(request, semester):
    if semester == 1:
        r = requests.get(FALL_URL)
    else:
        r = requests.get(SPRING_URL)

    root = lxml.html.fromstring(r.content)

    print root
    return HttpResponse("Success")
