from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.template import loader
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic import TemplateView
from django.core.serializers.json import DjangoJSONEncoder
from django.core.context_processors import csrf
from django.views.decorators.csrf import ensure_csrf_cookie
import datetime
from django.utils import timezone
from sets import Set

from ABET_DB.models import *
from django.http import HttpResponse, JsonResponse

def current():
    now = timezone.now()
    semNow = str()
    if now.month <= 5 and now.day < 14:
        semNow = "spring"
    elif now.month >= 7 and now.day > 10:
        semNow = "fall"
    else:
        semNow = "summer"
   
    return (semNow, now.year)

def professorPage(request):
    # after HARRY figures out security, this wont be needed
    # this should be passed in upon login
    request.session['netid'] = 'jkohann' 
    professorNetID = request.session['netid']
    
    sectionList = sections.objects.filter(professor__netID=professorNetID)
    
    # make a list of all semesters
    semesterSet = Set()
    for s in sectionList:
        syStr = s.semester +' '+ str(s.year)
        semesterSet.add(syStr)

    nowSem, nowYear = current()
    sectionsNow = sectionList.filter(semester=nowSem, year=nowYear)

    # run the template
    template = loader.get_template('ABET_DB/prof.html')
    context = {
        'netid':professorNetID,
        'semesters':list(semesterSet),
        'currentSem':nowSem +' '+ str(nowYear),
        'courses':sectionsNow,
    }
    return HttpResponse(template.render(context,request))

# this view returns a JSON list that is used for the right two menu bars of the app
def listJSON(request,what):
    print(what)
    
    professorNetID = request.session['netid']
    obj = dict()
    
    courseList = sections.objects.filter(professor__netID=professorNetID)     #find courses associated with loged-in professor
    
    semSem, semYear = tuple(request.GET['semStr'].split('_'))
    sectionsThisSem = courseList.filter(year=semYear).filter(semester=semSem)
    obj['semester'] = semSem
    obj['year'] = semYear
    obj['semStr'] = request.GET['semStr']
    
    if what == 'courses':
        obj['courses'] = list()
        for s in sectionsThisSem:
            obj['courses'].append(s.course.name)
    elif what == 'outcomes' or what == 'pis':
        courseName = request.GET['course'];
        obj['courseName'] = courseName
        
        section = sectionsThisSem.get(course__name=courseName)
        outcomeList = courseOutcomes.objects.filter(section=section)
        
        if what == 'outcomes':
            obj['outcomes'] = list()
            for o in outcomeList:
                obj['outcomes'].append(o.studentOutcome.outcomeLetter)
            print("outcome time!!")
        
        elif what == 'pis':
            print("pi time!!")
            outcomeLetter = request.GET['outcome']
            outcome = outcomeList.get(studentOutcome__outcomeLetter=outcomeLetter)
            obj['outcome'] = outcomeLetter
            piList = performanceIndicators.objects.filter(outcome__pk=outcome.id)
            obj['pis'] = list()
            for p in piList:
                obj['pis'].append(p.name)
            
    return JsonResponse(obj)
    
def form(request,what):
    
    professorNetID = request.session['netid']
    obj = dict()
    
    courseList = sections.objects.filter(professor__netID=professorNetID)     #find courses associated with loged-in professor
    semSem, semYear = tuple(request.GET['semStr'].split('_'))
    sectionsThisSem = courseList.filter(year=semYear).filter(semester=semSem)
    secton = sectionsThisSem.get(course__name=request.GET['course'])
    outcome = courseOutcomes.get(section__pk=section.id \
                                ,outcome__studentOutcome__outcomeLetter=request.GET['outcome'])
                                
                                
        

'''
def piForm(request,courseStr,outcome,pi="~"):
    
    professorNetID = request.session['netid']
    template = loader.get_template('ABET_DB/pi.html')
    
    course = courseStr.split('_')
    courseList = courses.objects.filter(professor__netID=professorNetID)     #find courses associated with loged-in professor
    
    c = courses.objects.filter(courseName=course[0]).filter(yr=int(course[2])).filter(semester=course[1]).first()
    outcomeList = studentOutcomes.objects.filter(course__id=c.id)
        
    try: o = outcomeList.get(outcomeLetter=outcome)
    except ObjectDoesNotExist:
        raise ValueError('outcome paramiter is not in list of outcomes for course')
        
    pis = performanceIndicators.objects.filter(outcome__outcomeLetter=outcome)      #find performance indicators associated with outcome
        
    piObject=None; rubricList=None
    if pi != '~':
        try:
            piObject = pis.get(name=pi)
            
        except ObjectDoesNotExist:
            raise ValueError('performance indicator paramiter not in list of performance indicators for outcomesd')
        rubricList = rubrics.objects.filter(performanceIndicator__name=pi)
    
    PLlist = performanceLevels.objects.all()
    
    context = {
        'course':c,
        'outcome':outcome,
        'pi':piObject,
        'rubrics':rubricList,
        'perfLevels':PLlist,
    }
    return HttpResponse(template.render(context,request))


def submitPi(request): # submit the data and reload the page
    
    # get all the stuff
    professorNetID = request.session['netid']
    courseList = courses.objects.filter(professor__netID=professorNetID)     #find courses associated with loged-in professor
    
    c3 = request.POST['course'].split('_');
    otext = request.POST['outcome']
    pitext = request.POST['name']
    
    
    try:
        c = courseList.filter(courseName=c3[0]).filter(yr=int(c3[2])).get(semester=c3[1])
        o = studentOutcomes.objects.get(course=c,outcomeLetter=otext)
        
    except ObjectDoesNotExist:
        raise ValueError("In submitPi, one object not found")
    
    (pi,created) = performanceIndicators.objects.update_or_create(name=pitext,outcome=o, \
            defaults={'weight':float(request.POST['weight']),
                      'description':request.POST['desc'],})
    
    for pl in performanceLevels.objects.all():
        a = str(pl.achievementLevel)
        if request.POST['r_'+a+'_upper'] and request.POST['r_'+a+'_lower']:
            rubrics.objects.update_or_create( \
                performanceIndicator__pk=pi.id,performanceLevel__id=pl.id, \
                defaults = {'gradeTopBound':int(request.POST['r_'+a+'_upper']),
                            'gradeLowerBound':int(request.POST['r_'+a+'_lower']),
                            'numStudents':int(request.POST['r_'+a+'_num']),
                            'description':request.POST['r_'+a+'_desc'],})
    
    return HttpResponse('hello')

def outcomeForm(request,courseStr,outcome):
    professorNetID = request.session['netid']
    template = loader.get_template('ABET_DB/outcome.html')
    
    course = courseStr.split('_')
    courseList = courses.objects.filter(professor__netID=professorNetID)     #find courses associated with loged-in professor
    
    c = courses.objects.filter(courseName=course[0]).filter(yr=int(course[2])).filter(semester=course[1]).first()
    outcomeList = studentOutcomes.objects.filter(course__id=c.id)
        
    try: o = outcomeList.get(outcomeLetter=outcome)
    except ObjectDoesNotExist:
        raise ValueError('outcome paramiter is not in list of outcomes for course')
        
    PLlist = performanceLevels.objects.all()
    
    context = {
        'course':c,
        'outcome':outcome,
        'perfLevels':PLlist,
    }
    return HttpResponse(template.render(context,request))

def submitOut(request):
    return HttpResponse("pass")
    
# this view returns a JSON list that is used for the right two menu bars of the app
def listJSON(request,courseStr,outcome='~'):
    professorNetID = request.session['netid']
    data = []
    course = courseStr.split('_')
    
    courseList = courses.objects.filter(professor__netID=professorNetID)     #find courses associated with loged-in professor
    if not courseList.exists():
        raise ValueError("No courses found for professor")
    outcomeList = studentOutcomes.objects.filter(course__courseName=course[0]).filter(course__yr=int(course[2])).filter(course__semester=course[1])
    
    
    # if we are asking for the outcomes
    if outcome == '~':
        for o in outcomeList:
            data.append({'letter':o.outcomeLetter, 'desc':o.description})
        obj = {'courseName':course[0],'data':data}
        
    # if we are asking for preformanc indicators
    else:
        pis = performanceIndicators.objects.filter(outcome__outcomeLetter=outcome)      #find performance indicators associated with outcome
        
        for p in pis:
            data.append({'name':p.name, 'id':p.id, 'desc':p.description})
        obj = {'courseName':course[0],'outcome':outcome,'data':data}
        
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

    
def populate(request):
    pass    
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
    rubA = rubrics(gradeTopBound=100, gradeLowerBound=90, description='Rubric A', numStudents=50, performanceLevel=excede, performanceIndicator=one)
    rubB = rubrics(gradeTopBound=90, gradeLowerBound=80, description='Rubric B', numStudents=50, performanceLevel=met, performanceIndicator=one)
    rubC = rubrics(gradeTopBound=80, gradeLowerBound=70, description='Rubric C', numStudents=50, performanceLevel=didNotMeet, performanceIndicator=one)
    rubD = rubrics(gradeTopBound=70, gradeLowerBound=0, description='Rubric D', numStudents=50, performanceLevel=failed, performanceIndicator=one)
    
    rubE = rubrics(gradeTopBound=100, gradeLowerBound=90, description='Rubric E', numStudents=50, performanceLevel=excede, performanceIndicator=two)
    rubF = rubrics(gradeTopBound=90, gradeLowerBound=80, description='Rubric F', numStudents=50, performanceLevel=met, performanceIndicator=two)
    rubG = rubrics(gradeTopBound=80, gradeLowerBound=70, description='Rubric G', numStudents=50, performanceLevel=didNotMeet, performanceIndicator=two)
    rubH = rubrics(gradeTopBound=70, gradeLowerBound=0, description='Rubric H', numStudents=50, performanceLevel=failed, performanceIndicator=two)
    
    rubI = rubrics(gradeTopBound=100, gradeLowerBound=90, description='Rubric I', numStudents=50, performanceLevel=excede, performanceIndicator=three)
    rubJ = rubrics(gradeTopBound=90, gradeLowerBound=80, description='Rubric J', numStudents=50, performanceLevel=met, performanceIndicator=three)
    rubK = rubrics(gradeTopBound=80, gradeLowerBound=70, description='Rubric K', numStudents=50, performanceLevel=didNotMeet, performanceIndicator=three)
    rubL = rubrics(gradeTopBound=70, gradeLowerBound=0, description='Rubric L', numStudents=50, performanceLevel=failed, performanceIndicator=three)
    
    rubm = rubrics(gradetopbound=100, gradelowerbound=90, description='rubric m', numstudents=50, performancelevel=excede, performanceindicator=four)
    rubN = rubrics(gradeTopBound=90, gradeLowerBound=80, description='Rubric N', numStudents=50, performanceLevel=met, performanceIndicator=four)
    rubO = rubrics(gradeTopBound=80, gradeLowerBound=70, description='Rubric O', numStudents=50, performanceLevel=didNotMeet, performanceIndicator=four)
    rubP = rubrics(gradeTopBound=70, gradeLowerBound=0, description='Rubric P', numStudents=50, performanceLevel=failed, performanceIndicator=four)
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
    rubK.save()
    rubL.save()
    rubM.save()
    rubN.save()
    rubO.save()
    rubP.save()
    return HttpResponse("Populated Database")
    
    
def clearDB(request):
    professors.objects.all().delete()
    courses.objects.all().delete()
    studentOutcomes.objects.all().delete()
    performanceLevels.objects.all().delete()
    rubrics.objects.all().delete()
    performanceIndicators.objects.all().delete()
    return HttpResponse("Cleared Database")
    
'''
    
