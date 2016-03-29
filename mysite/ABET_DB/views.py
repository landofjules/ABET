from django.shortcuts import render
from django.template import loader
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic import TemplateView
from ABET_DB import forms
from django.core.serializers.json import DjangoJSONEncoder


from ABET_DB.models import *
from django.http import HttpResponse, JsonResponse

    
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
    
    
def populate(request):
    
    #add professors
    jkohann = professors(netID='jkohann', isAdmin=False)
    bvz = professors(netID='bvz', isAdmin=True)
    ahnilica = professors(netID='ahnilica', isAdmin=False)
    jkohann.save()
    bvz.save()
    ahnilica.save()
    
    #add courses
    cs360 = courses(courseName='cs360', description='Systems Programing', yr=2016, semester='fall', professor=jkohann)
    cs140 = courses(courseName='cs140', description='Algorithms 1', yr=2016, semester='fall', professor=jkohann)
    cs420 = courses(courseName='cs420', description='Bio Inspired Computing', yr=2016, semester='fall', professor=jkohann)
    cs302 = courses(courseName='cs302', description='Algorithms 2', yr=2016, semester='fall', professor=bvz)
    cs102 = courses(courseName='cs102', description='Intro', yr=2016, semester='fall', professor=ahnilica)
    cs360.save()
    cs140.save()
    cs420.save()
    cs302.save()
    cs102.save()
    
    #add outcomes
    a = studentOutcomes(outcomeLetter='A', description='outcome A', course=cs360)
    b = studentOutcomes(outcomeLetter='B', description='outcome B', course=cs360)
    c = studentOutcomes(outcomeLetter='C', description='outcome C', course=cs140)
    d = studentOutcomes(outcomeLetter='D', description='outcome D', course=cs302)
    e = studentOutcomes(outcomeLetter='E', description='outcome E', course=cs302)
    f = studentOutcomes(outcomeLetter='F', description='outcome F', course=cs102)
    a.save()
    b.save()
    c.save()
    d.save()
    e.save()
    f.save()
    
    #add performanceIndicators
    one = performanceIndicators(name='one', weight=0.5, description='PI One', studentStrengths='Strength', studentWeaknesses='Weakness', outcome=a)
    two = performanceIndicators(name='two', weight=0.5, description='PI Two', studentStrengths='Strength', studentWeaknesses='Weakness', outcome=a)
    three = performanceIndicators(name='three', weight=0.5, description='PI three', studentStrengths='Strength', studentWeaknesses='Weakness', outcome=a)
    four = performanceIndicators(name='four', weight=0.5, description='PI four', studentStrengths='Strength', studentWeaknesses='Weakness', outcome=b)
    five = performanceIndicators(name='five', weight=0.5, description='PI five', studentStrengths='Strength', studentWeaknesses='Weakness', outcome=b)
    one.save()
    two.save()
    three.save()
    four.save()
    five.save()
    return HttpResponse("Populated Database")
    
    
def clearDB(request):
    professors.objects.all().delete()
    courses.objects.all().delete()
    studentOutcomes.objects.all().delete()
    return HttpResponse("Cleared Database")
    
    
def professorPage(request):
    # after harry figures out security, this wont be needed
    # this should be passed in upon login
    request.session['netid'] = 'jkohann' 
    
    profesorNetID = request.session['netid']
    
    courseList = courses.objects.filter(professor__netID=profesorNetID)
    
    # run the template
    template = loader.get_template('ABET_DB/prof.html')
    context = {
        'netid':profesorNetID,
        'courses':courseList,
    }
    return HttpResponse(template.render(context,request))


def pi(request,courseName,outcome,pi):
    
    professorNetID = request.session['netid']
    template = loader.get_template('ABET_DB/pi.html')
    
    courseList = courses.objects.filter(professor__netID=professorNetID)     #find courses associated with loged-in professor
        
    flag = 0
    for c in courseList:                                                    #make sure courseName paramiter is one of loged-in professor's courses
        if c.courseName == courseName:
            flag = 1
            
    if flag == 1:    
        outcomeList = studentOutcomes.objects.filter(course__courseName=courseName)         #find outcomes associated with course
            
    #else:
        #error Invalid course name in function paramiter, maybe raise exception
        
    flag = 0
    for o in outcomeList:                                                   #make sure outcome paramiter is in list of outcomes
        if o.outcomeLetter == outcome:
            flag = 1  
                
    #if flag != 1:
        #error Invalid outcome in function paramiter, maybe raise exception
        
    pis = performanceIndicators.objects.filter(outcome__outcomeLetter=outcome)      #find performance indicators associated with outcome
        
    flag = 0
    for p in pis:
        if p.name == pi:
            flag = 1
            
    #if flag != 1:
        #error
        
    rubricList = rubrics.objects.filter(performanceIndicator__name=pi)
    
    context = {
        'course':courseName,
        'outcome':outcome,
        'pi':pi,
        'rubrics':rubricList,
    }
    return HttpResponse(template.render(context,request))


# these will come
def submitPi(request): # submit the data and reload the page
    pass
def finalCount(request): # the final form we have to make
    pass
def submitFinal(request):
    pass


# this view returns a JSON list that is used for the right two menu bars of the app
def listJSON(request,courseName,outcome='~'):
    professorNetID = request.session['netid'] # ANDREW this is how we will remember the proffessor
    data = []
    
    # if we are asking for the outcomes
    if outcome == '~':
        courseList = courses.objects.filter(professor__netID=professorNetID)     #find courses associated with loged-in professor
        
        flag = 0
        for c in courseList:                                                    #make sure courseName paramiter is one of loged-in professor's courses
            if c.courseName == courseName:
                flag = 1
            
        if flag == 1:    
            outcomeList = studentOutcomes.objects.filter(course__courseName=courseName)         #find outcomes associated with course
            
        #else:
            #error Invalid course name, maybe raise exception
        
        for o in outcomeList:
            data.append({'letter':o.outcomeLetter, 'desc':o.description})
        obj = {'courseName':courseName,'data':data}
    else:
        courseList = courses.objects.filter(professor__netID=professorNetID)     #find courses associated with loged-in professor
        
        flag = 0
        for c in courseList:                                                    #make sure courseName paramiter is one of loged-in professor's courses
            if c.courseName == courseName:
                flag = 1
            
        if flag == 1:    
            outcomeList = studentOutcomes.objects.filter(course__courseName=courseName)         #find outcomes associated with course
            
        #else:
            #error Invalid course name in function paramiter, maybe raise exception
        
        flag = 0
        for o in outcomeList:                                                   #make sure outcome paramiter is in list of outcomes
            if o.outcomeLetter == outcome:
                flag = 1  
                
        #if flag != 1:
            #error Invalid outcome in function paramiter, maybe raise exception
        
        pis = performanceIndicators.objects.filter(outcome__outcomeLetter=outcome)      #find performance indicators associated with outcome
        
        for p in pis:
            data.append({'name':p.name, 'desc':p.description})
        obj = {'courseName':courseName,'outcome':outcome,'data':data}
        
    return JsonResponse(obj,safe=False)


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


class CreateContactView(CreateView):
    model = performanceLevels
    template_name = 'ABET_DB/edit_contact.html'
    form_class = forms.performanceLevelsForm
    
    
class UpdateContactView(UpdateView):
    model = performanceLevels
    template_name = 'edit_contact.html'
    form_class = forms.performanceLevelsForm
    
    
class AboutView(TemplateView):
    template_name = 'ABET_DB/about.html'

