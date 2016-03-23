from django.shortcuts import render
from django.template import loader

# Create your views here.
from ABET_DB.models import studentOutcomes, courses, performanceLevels
from django.http import HttpResponse

    
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
    
def professorPage(request):
    # after harry figures out security, this wont be needed
    # this should be passed in upon login
    request.session['netid'] = 'jkohann' 
    
    # retreive the information
    courseList = courses.objects.order_by('courseName')
    outcomeList = studentOutcomes.objects.order_by('outcomeLetter')
    
    # run the template
    template = loader.get_template('ABET_DB/prof.html')
    context = {
        'netid':request.session['netid'],
        'courses':courseList,
        'outcomes':outcomeList,
    }
    return HttpResponse(template.render(context,request))

def pi(request):
    # request should have:
    #    course
    template = loader.get_template('ABET_DB/pi.html')
    context = {
        
    }
    return HttpResponse(template.render(context,request))
    

def test1(request):
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

    

