import urllib2
import re
from django.http import HttpResponse
from django.template import loader, RequestContext
from django.shortcuts import get_object_or_404
from courses.models import Department, Course, Lab, Location, Instructor
import xml.etree.ElementTree as ET
from BeautifulSoup import BeautifulSoup, NavigableString


FALL_URL = "https://secure.upei.ca/cls/dropbox/FallTime.html"
SPRING_URL = "https://secure.upei.ca/cls/dropbox/SpringTime.html"

def semester_list(request, semester=1):
    courses_and_labs = []
    courses = Course.objects.filter(semester=semester).order_by("section").order_by("number")

    for course in courses:
        labs = Lab.objects.filter(course=course)
        courses_and_labs.append({
            "department": course.department,
            "number": course.number,
            "name": course.name,
            "instructor": course.instructor,
            "location": course.location,
            "labs": labs,
            })

    t = loader.get_template("list_courses.html")
    c = RequestContext(request, {
            "courses": courses_and_labs,
        })

    print dir(courses)
    return HttpResponse(t.render(c))

def dept_list(request, semester=1, dept=-1):
    print "hi?"
    department = get_object_or_404(Department, pk=dept)
    courses = Course.objects.filter(semester=semester).filter(department=department).order_by("section").order_by("number")
    t = loader.get_template("list_courses.html")
    c = RequestContext(request, {
            "courses": courses,
        })

    return HttpResponse(t.render(c))

## SCRAPING VIEWS ##
def scrape(request, semester):
    if semester == "2":
        print "SPRING"
        soup = BeautifulSoup(urllib2.urlopen(SPRING_URL))
    else:
        print "FALL"
        semester = "1"
        soup = BeautifulSoup(urllib2.urlopen(FALL_URL))

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

            # this area kind of makes me sad. I think I'll need to clean it up
            location_obj = Location.objects.filter(name=location)
            instructor_obj = Instructor.objects.filter(name=instructor)

            if len(location_obj) > 0:
                location_obj = location_obj[0]
            elif location and location != "&nbsp;":
                location_obj = Location.objects.create(name=location)
            else:
                location_obj = None

            if len(instructor_obj) > 0:
                instructor_obj = instructor_obj[0]
            elif instructor and instructor != "&nbsp;":
                instructor_obj = Instructor.objects.create(name=instructor)
            else:
                instructor_obj = None

            if isinstance(code, basestring):
                matchObj = re.match(r'^\D+', code)
                abbr = matchObj.group()
                depts = Department.objects.filter(abbr=abbr)

                if is_letter(code[-1]):
                    section = code[-1]
                else:
                    section = None

                # create the department if it doesnt exist
                if len(depts) == 0:
                    dept = Department(abbr=abbr)
                    dept.save()
                else:
                    dept = depts[0]

                num = re.findall(r'\d+', code)
                course = Course(department=dept, number=num[0], name=name,
                        semester=semester, section=section, instructor=instructor_obj,
                        location=location_obj)
                course.save()

            else:
                matchObj = re.match('^\D+', code[0])
                abbr = matchObj.group()
                depts = Department.objects.filter(abbr=abbr)

                if is_letter(code[0][-1]):
                    section = code[0][-1]
                else:
                    section = None

                if len(depts) == 0:
                    dept = Department(abbr=abbr)
                    dept.save()
                else:
                    dept = depts[0]
                # deal with the actual specific course now
                num = re.findall('\d+', code[0])
                course = Course(department=dept, number=num[0], name=name,
                        semester=semester, section=section, instructor=instructor_obj,
                        location=location_obj)
                course.save()

    for row in lab_rows:
        columns = row.findAll("td")
        if len(columns)>0:
            code = parse_course_code(columns[0])

            deptMatch = re.match('^\D+', code)
            dept = deptMatch.group()

            numMatch = re.findall('\d+', code)
            num = numMatch[0]

            department = Department.objects.filter(abbr=str(dept))
            if len(department) > 0:
                course = Course.objects.filter(number=num).filter(department=department[0])

                if len(course)>0:
                    Lab.objects.create(course=course[0])

    return HttpResponse("Success")



def parse_course_code(code):
    if code.string == None:

        # removes all of the characters mentioned in the given string
        # the translate function makes my life better
        code = str(code).translate(None, "cl.<>/tdb r*") 
        code_list = code.split("(")
        return map(lambda c: "".join(c.split()).translate(None, ")"), code_list)
    else:
        return code.string.replace(" ", "")

def is_letter(s):
    try:
        float(s)
        return False
    except ValueError:
        return True
