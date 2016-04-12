from django.contrib import admin

# Register your models here.
from ABET_DB.models import *

class professorAdmin(admin.ModelAdmin):
    search_fields = ('ln', 'fn')
    ordering = ('ln', 'fn')
    
class studentOutcomeAdmin(admin.ModelAdmin):
    search_fields = ('outcomeLetter',)
    ordering = ('outcomeLetter',)

class courseAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    ordering = ('name',)
    
class sectionAdmin(admin.ModelAdmin):
    search_fields = ('course', 'year', 'semester')
    ordering = ('-year', 'semester', 'course')
    
class outcomeDataAdmin(admin.ModelAdmin):
    search_fields = ('outcome',)
    ordering = ('outcome',)

class performanceLevelAdmin(admin.ModelAdmin):
    search_fields = ('description',)
    ordering = ('description',)

class courseOutcomeAdmin(admin.ModelAdmin):
    search_fields = ('studentOutcome', 'section')
    ordering = ('studentOutcome', 'section')

admin.site.register(sections, sectionAdmin)
admin.site.register(courseOutcomes, courseOutcomeAdmin)

admin.site.register(performanceLevels, performanceLevelAdmin)
admin.site.register(studentOutcomes, studentOutcomeAdmin)
admin.site.register(professors, professorAdmin)
admin.site.register(courses, courseAdmin)


