from django.contrib import admin

# Register your models here.
from ABET_DB.models import performanceLevels, performanceIndicators
from ABET_DB.models import studentOutcomes, rubrics
from ABET_DB.models import outcomeData, courses, professors

admin.site.register(performanceLevels)
admin.site.register(performanceIndicators)
admin.site.register(outcomeData)
admin.site.register(studentOutcomes)
admin.site.register(rubrics)
admin.site.register(courses)
admin.site.register(professors)
