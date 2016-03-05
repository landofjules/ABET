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
    courseList = courses.objects.order_by('courseName')
    
    if len(courseList) == 0:
        str2 = '&nbsp;&nbsp;&nbsp;NONE<br><br>'
    else:
        str2 = '&nbsp;&nbsp;&nbsp;' + ', '.join([q.courseName for q in courseList]) + '<br><br>'
        
    title3 = 'performanceLevels: achievementLevel<br><br>'
    performanceList = performanceLevels.objects.order_by('achievementLevel')
    
    if len(performanceList) == 0:
        str3 = '&nbsp;&nbsp;&nbsp;NONE<br><br>'
    else:
        str3 = '&nbsp;&nbsp;&nbsp;' + ', '.join([str(q.achievementLevel) for q in performanceList]) + '<br><br>'
    
    output = title1 + str1 + title2+ str2 + title3 + str3
    return HttpResponse(output)
    
    
def showDataTemplate(request):
    
    outcomeList = studentOutcomes.objects.order_by('outcomeLetter')
    courseList = courses.objects.order_by('courseName')
    performanceList = performanceLevels.objects.order_by('achievementLevel')
    
    template = loader.get_template('ABET_DB/showDataTemplate.html')
    
    context = {
      'outcomeList': outcomeList,
      'courseList': courseList,
      'performanceList': performanceList,
    }
    
    return HttpResponse(template.render(context, request))
    


def index(request):
    # gather the information and add it to to database
    if request.method=='POST':
        dat = request.POST
        print(dat.dict())
        # studentOutcomes, courses, performanceLevels
        if dat.__contains__("OutcomeLetter"):
            ol = studentOutcomes()
            ol.outcomeLetter = dat.get("OutcomeLetter")
            ol.description = dat.get("description")
            ol.save()
        elif dat.__contains__("AchLevel"):
            a = performanceLevels()
            a.achievementLevel = dat.get("AchLevel")
            a.description = dat.get("description")
            a.save()
        elif  dat.__contains__("CourseName"):
            c = courses()
            c.crnNumber = dat.get("crn")
            c.courseName = dat.get("CourseName")
            c.description = dat.get("description")
            c.save()
    #load the data as usual
    template = loader.get_template('ABET_DB/index.html')
    outcomeList = studentOutcomes.objects.order_by('outcomeLetter')
    courseList = courses.objects.order_by('courseName')
    perfList = performanceLevels.objects.order_by('achievementLevel')
    context = {
        'outcomeList':outcomeList,
        'courseList':courseList,
        'perfList':perfList,
    }
    return HttpResponse(template.render(context,request))

    
# one view w 3 boxes:
#   StudentOutcomes : outcomeLetters, descripeion
#   PreformanceLevels : aceivementLevel, description
#   Courses : CRNnumber, CourseName, course_description

