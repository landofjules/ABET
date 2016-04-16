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
    

admin.site.register(sections, sectionAdmin)
admin.site.register(courseOutcomes, courseOutcomeAdmin)

admin.site.register(performanceLevels, performanceLevelAdmin)
admin.site.register(studentOutcomes, studentOutcomeAdmin)
admin.site.register(professors, professorAdmin)
admin.site.register(courses, courseAdmin)


