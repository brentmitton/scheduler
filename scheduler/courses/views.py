from courses.models import Department, Course, Lab
import xml.etree.ElementTree as ET
from django.http import HttpResponse
from BeautifulSoup import BeautifulSoup, NavigableString
import urllib2
import re

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
            code = parse_course_code(columns[0])
            name = columns[1].string
            location = columns[2].string
            time = columns[3].string
            status = columns[4].string
            instructor = columns[5].string


            if isinstance(code, basestring):
                matchObj = re.match(r'^\D+', code)
                abbr = matchObj.group()
                depts = Department.objects.filter(abbr=abbr)

                # create the department if it doesnt exist
                if len(depts) == 0:
                    dept = Department(abbr=abbr)
                    dept.save()
                else:
                    dept = depts[0]

                num = re.findall(r'\d+', code)
                print num
                course = Course(department=dept, number=num[0], name=name)
                course.save()

            else:
                for c in code:
                    matchObj = re.match('^\D+', c)
                    abbr = matchObj.group()
                    depts = Department.objects.filter(abbr=abbr)
                    if len(depts) == 0:
                        dept = Department(abbr=abbr)
                        dept.save()
                    else:
                        dept = depts[0]
                    # deal with the actual specific course now
                    num = re.findall('\d+', c)
                    print num
                    course = Course(department=dept, number=num[0], name=name)
                    course.save()

    return HttpResponse("Success")



def parse_course_code(code):
    if code.string == None:

        # removes all of the characters mentioned in the given string
        # the translate function makes my life better
        code = str(code).translate(None, "cl.<>/tdb r") 
        print "code: %s" %(code)
        code_list = code.split("(")
        return map(lambda c: "".join(c.split()).translate(None, ")"), code_list)
    else:
        return code.string.replace(" ", "")
