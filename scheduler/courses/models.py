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

class Department(models.Model):
    abbr = models.CharField(max_length=10)
    name = models.CharField(max_length=70, blank=True, null=True)
    faculty = models.CharField(max_length=2, choices=FACULTIES, blank=True, null=True)

class Course(models.Model):
    department = models.ForeignKey(Department)
    number = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

class Lab(models.Model):
    course = models.ForeignKey(Course)



