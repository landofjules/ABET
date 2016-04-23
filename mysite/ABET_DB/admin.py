from django.contrib import admin
from ABET_DB.models import *

class professorAdmin(admin.ModelAdmin):
    search_fields = ('ln', 'fn', 'netID')
    ordering = ('ln', 'fn')
    list_display = ('ln', 'fn', 'netID')
    
    
class studentOutcomeAdmin(admin.ModelAdmin):
    search_fields = ('outcomeLetter',)
    ordering = ('outcomeLetter',)
  

class courseAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    ordering = ('name',)
   
    
class sectionAdmin(admin.ModelAdmin):
    search_fields = ('course__name', 'professor__ln', 'professor__fn', 'year', 'semester')
    ordering = ('-year', '-semester', 'course', 'professor')
    list_display = ('year', 'semester', 'course', 'professor')
    

class performanceLevelAdmin(admin.ModelAdmin):
    ordering = ('achievementLevel', 'description')
    list_display = ('achievementLevel', 'description')
   

class courseOutcomeAdmin(admin.ModelAdmin):
    search_fields = ('studentOutcome__outcomeLetter', 'section__year', 'section__semester')
    ordering = ('-section__year', '-section__semester', 'studentOutcome__outcomeLetter')
    list_display = ('studentOutcome', 'section')
    

class outcomeDataAdmin(admin.ModelAdmin):
    ordering = ('outcome', 'performanceLevel')
    list_display = ('outcome', 'performanceLevel')
    
    
class performanceIndicatorAdmin(admin.ModelAdmin):
    ordering = ('outcome', 'name')
    list_display = ('outcome', 'name')
    
    
class rubricAdmin(admin.ModelAdmin):
    ordering = ('performanceIndicator', 'performanceLevel')
    list_display = ('performanceIndicator', 'performanceLevel')


admin.site.register(sections, sectionAdmin)
admin.site.register(courseOutcomes, courseOutcomeAdmin)

admin.site.register(performanceLevels, performanceLevelAdmin)
admin.site.register(studentOutcomes, studentOutcomeAdmin)
admin.site.register(professors, professorAdmin)
admin.site.register(courses, courseAdmin)

admin.site.register(outcomeData, outcomeDataAdmin)
admin.site.register(performanceIndicators, performanceIndicatorAdmin)
admin.site.register(rubrics, rubricAdmin)



