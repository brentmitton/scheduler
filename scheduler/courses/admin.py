from django.contrib import admin
from courses.models import Department, Course, Lab, Instructor, Location

admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Lab)
admin.site.register(Location)
admin.site.register(Instructor)
