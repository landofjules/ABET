from django.shortcuts import render
from django.template import loader

# Create your views here.
from ABET_DB.models import studentOutcomes, courses, performanceLevels
from django.http import HttpResponse


def showData(request):
    
    title1 = 'studentOutcomes: outcomeLetter<br><br>'
    outcomeList = studentOutcomes.objects.order_by('outcomeLetter')
    
    if len(outcomeList) == 0:
        str1 = '&nbsp;&nbsp;&nbsp;NONE<br><br>'
    else:
        str1 = '&nbsp;&nbsp;&nbsp;' + ', '.join([q.outcomeLetter for q in outcomeList]) + '<br><br>'
    
    title2 = 'courses: courseName<br><br>'
    outcomeList = courses.objects.order_by('courseName')
    
    if len(outcomeList) == 0:
        str2 = '&nbsp;&nbsp;&nbsp;NONE<br><br>'
    else:
        str2 = '&nbsp;&nbsp;&nbsp;' + ', '.join([q.courseName for q in outcomeList]) + '<br><br>'
        
    title3 = 'performanceLevels: achievementLevel<br><br>'
    outcomeList = performanceLevels.objects.order_by('achievementLevel')
    
    if len(outcomeList) == 0:
        str3 = '&nbsp;&nbsp;&nbsp;NONE<br><br>'
    else:
        str3 = '&nbsp;&nbsp;&nbsp;' + ', '.join([str(q.achievementLevel) for q in outcomeList]) + '<br><br>'
    
    output = title1 + str1 + title2+ str2 + title3 + str3
    return HttpResponse(output)


def index(request):
    template = loader.get_template('ABET_DB/index.html')
    return HttpResponse(template.render())

    
# one view w 3 boxes:
#   StudentOutcomes : outcomeLetters, descripeion
#   PreformanceLevels : aceivementLevel, description
#   Courses : CRNnumber, CourseName, course_description

