from django.db import models

FACULTIES = (
        ("A", "Arts"),
        ("B", "Business"),
        ("E", "Education"),
        ("N", "Nursing"),
        ("S", "Science"),
        ("V", "Veterinary Medicine"),
        ("O", "Other"),
        )

SEMESTER = (
        ("1", "Fall Semester"),
        ("2", "Spring Semester"),
        )

# Department might not actually be a department, for instance
# UNIV courses.
class Department(models.Model):
    abbr = models.CharField(max_length=10)
    name = models.CharField(max_length=70, blank=True, null=True)
    faculty = models.CharField(max_length=2, choices=FACULTIES, blank=True, null=True)

    def __unicode__(self):
        return self.abbr

class Instructor(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return "%s" %(self.name)

class Location(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

class Course(models.Model):
    department = models.ForeignKey(Department)
    number = models.CharField(max_length=10)
    name = models.CharField(max_length=100, default="No course name given", null=True)
    section = models.CharField(max_length=1,blank=True, null=True)
    semester = models.CharField(max_length=1, choices=SEMESTER)
    instructor = models.ForeignKey(Instructor, null=True, blank=True)
    location = models.ForeignKey(Location, null=True, blank=True)
    start_time = models.IntegerField(null=True, blank=True)
    end_time= models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        if self.section is not None:
            return "%s %s%s -- %s" %(self.department.abbr, self.number, self.section, self.name)
        else:
            return "%s %s -- %s" %(self.department.abbr, self.number, self.name)

class Lab(models.Model):
    course = models.ForeignKey(Course)
    name = models.CharField(max_length=10, null=True, blank=True)

    def __unicode__(self):
        return "%s" %(self.course)




