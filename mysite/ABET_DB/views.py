from django.shortcuts import render
from django.template import loader

# Create your views here.
from ABET_DB.models import studentOutcomes, courses, performanceLevels
from django.http import HttpResponse


def showData(request):
    
    title1 = 'studentOutcomes: outcomeLetter<br><br>'
    outcomeList = studentOutcomes.objects.order_by('outcomeLetter')
    
    if len(outcomeList) == 0:
        str1 = '&nbsp;&nbsp;&nbsp;NONE<br>'
    else:
        str1 = '&nbsp;&nbsp;&nbsp;' + ', '.join([q.outcomeLetter for q in outcomeList]) + '<br>'
    
    title2 = 'courses: courseName<br><br>'
    outcomeList = courses.objects.order_by('courseName')
    
    if len(outcomeList) == 0:
        str2 = '&nbsp;&nbsp;&nbsp;NONE<br>'
    else:
        str2 = '&nbsp;&nbsp;&nbsp;' + ', '.join([q.courseName for q in outcomeList]) + '<br>'
        
    title3 = 'performanceLevels: achievementLevel<br>'
    outcomeList = performanceLevels.objects.order_by('achievementLevel')
    
    if len(outcomeList) == 0:
        str3 = '&nbsp;&nbsp;&nbsp;NONE<br><br>'
    else:
        str3 = '&nbsp;&nbsp;&nbsp;' + ', '.join([str(q.achievementLevel) for q in outcomeList]) + '<br>'
    
    output = title1 + str1 + title2+ str2 + title3 + str3
    return HttpResponse(output)


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
        elif dat.__contains__("AcheivementLevel"):
            a = performanceLevels()
            a.weight = dat.get("PerfLevel")
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

