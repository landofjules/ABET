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
    
    #add performanceLevels
    excede = performanceLevels(achievementLevel=0, description='Exceded Expectations')
    met = performanceLevels(achievementLevel=1, description='Met Expectations')
    didNotMeet = performanceLevels(achievementLevel=2, description='Did Not Meet Expectations')
    failed = performanceLevels(achievementLevel=3, description='Performed Poorly')
    excede.save()
    met.save()
    didNotMeet.save()
    failed.save()
    
    #add professors
    jkohann = professors(netID='jkohann', isAdmin=False)
    bvz = professors(netID='bvz', isAdmin=True)
    ahnilica = professors(netID='ahnilica', isAdmin=False)
    stonecoldhughes = professors(netID='stonecoldhughes', isAdmin=False)
    jkohann.save()
    bvz.save()
    ahnilica.save()
    stonecoldhughes.save()
    
    #add courses
    cs360 = courses(courseName='cs360', description='Systems Programing', yr=2016, semester='fall', professor=jkohann)
    cs140 = courses(courseName='cs140', description='Algorithms 1', yr=2016, semester='fall', professor=jkohann)
    cs420 = courses(courseName='cs420', description='Bio Inspired Computing', yr=2016, semester='fall', professor=jkohann)
    cs401 = courses(courseName='cs401', description='Sr Design Theory', yr=2016, semester='fall', professor=jkohann)
    cs402 = courses(courseName='cs402', description='Sr Design Practicum', yr=2016, semester='fall', professor=jkohann)
    cs302 = courses(courseName='cs302', description='Algorithms 2', yr=2016, semester='fall', professor=bvz)
    cs102 = courses(courseName='cs102', description='Intro', yr=2016, semester='fall', professor=ahnilica)
    cs360.save()
    cs140.save()
    cs420.save()
    cs401.save()
    cs402.save()
    cs302.save()
    cs102.save()
    
    #add outcomes
    a = studentOutcomes(outcomeLetter='A', description='outcome A', course=cs360)
    b = studentOutcomes(outcomeLetter='B', description='outcome B', course=cs360)
    c = studentOutcomes(outcomeLetter='C', description='outcome C', course=cs140)
    d = studentOutcomes(outcomeLetter='D', description='outcome D', course=cs302)
    e = studentOutcomes(outcomeLetter='E', description='outcome E', course=cs302)
    f = studentOutcomes(outcomeLetter='F', description='outcome F', course=cs102)
    g = studentOutcomes(outcomeLetter='G', description='outcome G', course=cs140)
    h = studentOutcomes(outcomeLetter='H', description='outcome H', course=cs420)
    i = studentOutcomes(outcomeLetter='I', description='outcome I', course=cs140)
    j = studentOutcomes(outcomeLetter='J', description='outcome J', course=cs402)
    a.save()
    b.save()
    c.save()
    d.save()
    e.save()
    f.save()
    g.save()
    h.save()
    i.save()
    j.save()
    
    #add performanceIndicators
    one = performanceIndicators(name='one', weight=0.5, description='PI One', studentStrengths='Strength', studentWeaknesses='Weakness', outcome=a)
    two = performanceIndicators(name='two', weight=0.5, description='PI Two', studentStrengths='Strength', studentWeaknesses='Weakness', outcome=a)
    three = performanceIndicators(name='three', weight=0.5, description='PI three', studentStrengths='Strength', studentWeaknesses='Weakness', outcome=a)
    four = performanceIndicators(name='four', weight=0.5, description='PI four', studentStrengths='Strength', studentWeaknesses='Weakness', outcome=b)
    five = performanceIndicators(name='five', weight=0.5, description='PI five', studentStrengths='Strength', studentWeaknesses='Weakness', outcome=b)
    six = performanceIndicators(name='six', weight=0.5, description='PI six', studentStrengths='Strength', studentWeaknesses='Weakness', outcome=c)
    seven = performanceIndicators(name='seven', weight=0.5, description='PI seven', studentStrengths='Strength', studentWeaknesses='Weakness', outcome=c)
    eight = performanceIndicators(name='eight', weight=0.5, description='PI eight', studentStrengths='Strength', studentWeaknesses='Weakness', outcome=a)
    nine = performanceIndicators(name='nine', weight=0.5, description='PI nine', studentStrengths='Strength', studentWeaknesses='Weakness', outcome=b)
    ten = performanceIndicators(name='ten', weight=0.5, description='PI ten', studentStrengths='Strength', studentWeaknesses='Weakness', outcome=b)
    one.save()
    two.save()
    three.save()
    four.save()
    five.save()
    six.save()
    seven.save()
    eight.save()
    nine.save()
    ten.save()
    
    #add rubrics
    rubA = rubrics(gradeTopBound=100, gradeLowerBound=90, description='Rubric A', numStudents=50, performanceIndicator=one)
    rubB = rubrics(gradeTopBound=90, gradeLowerBound=80, description='Rubric B', numStudents=50, performanceIndicator=one)
    rubC = rubrics(gradeTopBound=80, gradeLowerBound=70, description='Rubric C', numStudents=50, performanceIndicator=one)
    rubD = rubrics(gradeTopBound=100, gradeLowerBound=90, description='Rubric D', numStudents=50, performanceIndicator=two)
    rubE = rubrics(gradeTopBound=90, gradeLowerBound=80, description='Rubric E', numStudents=50, performanceIndicator=two)
    rubF = rubrics(gradeTopBound=90, gradeLowerBound=80, description='Rubric F', numStudents=50, performanceIndicator=three)
    rubG = rubrics(gradeTopBound=90, gradeLowerBound=80, description='Rubric G', numStudents=50, performanceIndicator=three)
    rubH = rubrics(gradeTopBound=90, gradeLowerBound=80, description='Rubric H', numStudents=50, performanceIndicator=three)
    rubI = rubrics(gradeTopBound=90, gradeLowerBound=80, description='Rubric I', numStudents=50, performanceIndicator=four)
    rubJ = rubrics(gradeTopBound=90, gradeLowerBound=80, description='Rubric J', numStudents=50, performanceIndicator=four)
    rubA.save()
    rubB.save()
    rubC.save()
    rubD.save()
    rubE.save()
    rubF.save()
    rubG.save()
    rubH.save()
    rubI.save()
    rubJ.save()
    return HttpResponse("Populated Database")
    
    
def clearDB(request):
    professors.objects.all().delete()
    courses.objects.all().delete()
    studentOutcomes.objects.all().delete()
    performanceLevels.objects.all().delete()
    rubrics.objects.all().delete()
    performanceIndicators.objects.all().delete()
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
            
    else:
        raise ValueError('courseName paramiter is not in list of courses for professor')
        
    flag = 0
    for o in outcomeList:                                                   #make sure outcome paramiter is in list of outcomes
        if o.outcomeLetter == outcome:
            flag = 1  
                
    if flag != 1:
        raise ValueError('outcome paramiter is not in list of outcomes for course')
        
    pis = performanceIndicators.objects.filter(outcome__outcomeLetter=outcome)      #find performance indicators associated with outcome
        
    flag = 0
    for p in pis:
        if p.name == pi:
            flag = 1
            
    if flag != 1:
        raise ValueError('performance indicator paramiter not in list of performance indicators for outcomesd')
        
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
    professorNetID = request.session['netid']
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
            
        else:
            raise ValueError('courseName paramiter is not in list of courses for professor')
        
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
            
        else:
            raise ValueError('courseName paramiter is not in list of courses for professor')
            
        flag = 0
        for o in outcomeList:                                                   #make sure outcome paramiter is in list of outcomes
            if o.outcomeLetter == outcome:
                flag = 1  
                
        if flag != 1:
            raise ValueError('outcome paramiter is not in list of outcomes for course')
        
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

