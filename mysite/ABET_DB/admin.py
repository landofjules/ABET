from django.contrib import admin

# Register your models here.
from ABET_DB.models import *

admin.site.register(professors)
admin.site.register(performanceLevels)
admin.site.register(courses)
admin.site.register(sections)
admin.site.register(outcomeData)
admin.site.register(studentOutcomes)
admin.site.register(performanceIndicators)
admin.site.register(rubrics)
admin.site.register(courseOutcomes)

