from django.contrib import admin

# Register your models here.
from ABET_DB.models import *

admin.site.register(professor)
admin.site.register(performanceLevel)
admin.site.register(course)
admin.site.register(section)
admin.site.register(outcomeData)
admin.site.register(studentOutcome)
admin.site.register(performanceIndicator)
admin.site.register(rubric)
admin.site.register(courseOutcome)

