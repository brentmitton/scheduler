from courses.models import Department, Course, Lab
import xml.etree.ElementTree as ET
from django.http import HttpResponse
from BeautifulSoup import BeautifulSoup, NavigableString
import urllib2

FALL_URL = "https://secure.upei.ca/cls/dropbox/FallTime.html"
SPRING_URL = "https://secure.upei.ca/cls/dropbox/SpringTime.html"

def scrape(request, semester):
    if semester == 1:
        soup = BeautifulSoup(urllib2.urlopen(FALL_URL))
    else:
        soup = BeautifulSoup(urllib2.urlopen(SPRING_URL))

    tables = soup.findAll('table',attrs={"width":"100%"})
    table = tables[0]

    # get all non-lab rows
    course_rows = table.findAll(lambda tag: tag.name == "tr" and not tag.attrs)
    lab_rows = table.findAll(lambda tag: tag.name == "tr" and tag.attrs)

    for row in course_rows:
        columns = row.findAll("td")
        if len(columns)>0:
            print "Code: %s -- Name: %s -- Location: %s -- Time: %s --  Status: %s -- Instructor: %s" %(parse_course_code(columns[0]), columns[1].string, columns[2].string, columns[3].string, columns[4].string, columns[5].string)
    return HttpResponse("Success")

def parse_course_code(code):
    if code.string == None:
        code_list = str(code).split("<br />")
        cleaned_string = " ".join(code_list)
        print cleaned_string
    else:
        return code.string
