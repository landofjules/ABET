from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.template import loader
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic import TemplateView
from django.core.serializers.json import DjangoJSONEncoder
from django.core.context_processors import csrf
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http.response import HttpResponseRedirect
#from django.utils import timezone
from sets import Set
from ABET_DB.exceptions import ABET_Error
from decimal import *
import pdb


from ABET_DB.models import *
from django.http import HttpResponse, JsonResponse



MAIN_PASSWORD = 'hello'

def login(request, context={}):
    
    template = loader.get_template('ABET_DB/login.html')
    
    if request.method == 'POST':
        netid = request.POST['netid']
        password = request.POST['password']
        
        try:
            professors.objects.get(netID=netid)
            
            # Eventually, LDAP will be setup here
            if password != MAIN_PASSWORD:
                raise ObjectDoesNotExist
        except ObjectDoesNotExist:
            context['errors'] = True
        else:
            context['errors'] = False
            request.session['netid'] = netid 
            return HttpResponseRedirect('prof/')
    
    
    return HttpResponse(template.render(context,request))

def logout(request):
    del request.session['netid']
    return HttpResponseRedirect('/')
    

# this view returns the main page for professors entering data
def professorPage(request):
    
    
    # # #   Build the page   # # #
    try:
        professorNetID = request.session['netid']
    except KeyError:
        return HttpResponseRedirect('/')
    
    # return a query of all professor's sections
    sectionList = sections.objects.filter(professor__netID=professorNetID).order_by("-year","semester")
    
    # make a list of all semesters for drop down
    semList = list()
    for s in sectionList:
        syStr = s.semester +' '+ str(s.year)
        if syStr not in semList:
            semList.append(syStr)

    # get the current semester and year and select sections for it
    #pdb.set_trace()
    if sectionList:
        thisYear = sectionList[0].year
        thisSemester = sectionList[0].semester
    else:
        thisSemester, thisYear = current()
    sectionsThisSem = sectionList.filter(semester=thisSemester, year=thisYear)
    
    # retrieve performance indicators
    perfLevList = performanceLevels.objects.all()

    # load the template and provide it the nessecary information
    template = loader.get_template('ABET_DB/prof.html')
    context = {
        'netid':professorNetID,
        'semesters':semList,
        'currentSem':thisSemester+' '+ str(thisYear),
        'courses':sectionsThisSem,
        'perfLevels':perfLevList,
    }
    return HttpResponse(template.render(context,request))

# this view returns a JSON list that is used for the right two menu bars of the app and the course list
def listJSON(request,what):
    
    professorNetID = request.session['netid']
    obj = dict()
    
    # retreive professors list of courses
    courseList = sections.objects.filter(professor__netID=professorNetID)     #find courses associated with loged-in professor
    
    # retreive client specified semester and year, then filter sections accordingly
    semSem, semYear = tuple(request.GET['semStr'].split('_'))
    sectionsThisSem = courseList.filter(year=semYear).filter(semester=semSem)
    obj['semester'] = semSem
    obj['year'] = semYear
    obj['semStr'] = request.GET['semStr']
    
    # return specified content based on url
    if what == 'courses':
        
        # return a list of course names for specified semester
        obj['courses'] = list()
        for s in sectionsThisSem:
            obj['courses'].append(s.course.name)
            
    elif what == 'outcomes' or what == 'pis':
        
        # retreive the outcomes for the selected course
        courseName = request.GET['course']
        obj['courseName'] = courseName
        section = sectionsThisSem.get(course__name=courseName)
        outcomeList = courseOutcomes.objects.filter(section=section)
        
        # if client asks for the outcomes, then simply return that list
        if what == 'outcomes':
            obj['outcomes'] = list()
            for o in outcomeList:
                obj['outcomes'].append(o.studentOutcome.outcomeLetter)
        
        # if client is asking for performance indicators...
        elif what == 'pis':
            
            
            # retrieve the outcome, and filter pis based on that list
            outcomeLetter = request.GET['outcome']
            outcome = outcomeList.get(studentOutcome__outcomeLetter=outcomeLetter)
            obj['outcome'] = outcomeLetter
            # data for the outcome description on top of form place
            obj['outcomeDesc'] = outcome.studentOutcome.description;
            piList = performanceIndicators.objects.filter(outcome__pk=outcome.id)
            obj['pis'] = list()
            for p in piList:
                obj['pis'].append(p.name)
            
            # append objects semester years for populate
            outcomesOfSemesters = courseOutcomes.objects.filter(studentOutcome__outcomeLetter=outcomeLetter) \
                                                        .filter(section__course__name=courseName)
            
            obj['piSems'] = list()
            for oos in outcomesOfSemesters:
                obj['piSems'].append(oos.section.semester + ' ' + str(oos.section.year) )
            
    return JsonResponse(obj)

def prevPis(request):
    print "hello"
    
    professorNetID = request.session['netid']
    courseName = request.GET['course']
    outcome = request.GET['outcome']
    courseList = sections.objects.filter(professor__netID=professorNetID)     #find courses associated with loged-in professor
    
    perfLevels = performanceLevels.objects.all()
    
    thisSem, thisYear = tuple(request.GET['semStr'].split('_'))
    selectedSem, selectedYear = tuple(request.GET['selectedSemStr'].split('_'))
    
    sectionsThisSem = courseList.filter(year=thisYear).filter(semester=thisSem)
    sectionsSelSem = courseList.filter(year=selectedYear).filter(semester=selectedSem)
    try:
        thisSection = sectionsThisSem.get(course__name=courseName)
        selSection = sectionsSelSem.get(course__name=courseName)
    
        thisOutcome = courseOutcomes.objects.filter(section=thisSection).get(studentOutcome__outcomeLetter=outcome)
        selOutcome = courseOutcomes.objects.filter(section=selSection).get(studentOutcome__outcomeLetter=outcome)
        
    except ObjectDoesNotExist:
        return JsonResponse({'success':False})
    
    # get all the pis, from sel outcome and append them to thisOutcome
    selectedPis = performanceIndicators.objects.filter(outcome=selOutcome)
    thesePis = performanceIndicators.objects.filter(outcome=thisOutcome)
    for spi in selectedPis:
        
        if thesePis.filter(name=spi.name).exists():
            tpi = thesePis.get(name=spi.name)
            rubricsHere = rubrics.objects.filter(performanceIndicator=tpi)
        else:
            tpi = selectedPis.get(name=spi.name)
            tpi.id = None
            tpi.outcome = thisOutcome
            tpi.save()
            rubricsHere = rubrics.objects.filter(performanceIndicator=spi)
            for r in rubricsHere:
                r.id = None
                r.performanceIndicator = tpi
                r.save()
        
    
    return JsonResponse({'success':True})
    
def graph(request):
    #get the student outcomes
    getcontext().prec = 3
    outcomeList = courseOutcomes.objects.all()
    
    #get all outcomes
    rubricList = rubrics.objects.all()
    
    outcomeResults = []
    #go through each outcome and group everything by the outcome
    for outcome in outcomeList:
        sectionName = ""
        sectionName = outcome.section.course.name + " " + str(outcome.section.semester) + ", " + str(outcome.section.year)
        outcomeObject = {
            'section': sectionName,
            'letter': outcome.studentOutcome.outcomeLetter,
            'rubricList': [],
            'exceeded': Decimal(0),
            'met': Decimal(0),
            'total': Decimal(0)
        }

        rList = []
        
        for rubric in rubricList:
            #make sure the selection is only comparing similar outcomes
            if (rubric.performanceIndicator.outcome.id != outcome.id):
                continue
            
            rubricObject = {
                'perfID': rubric.performanceIndicator.id,
                'met': 0,
                'exceeded': 0,
                'below': 0,
                'weight': rubric.performanceIndicator.weight,
                'total': 0
            }
            #see if rubric already exists in rubric list
            for r in rList:
                if (r['perfID'] == rubric.performanceIndicator.id):
                    rubricObject = r
                    break
            
            #achievment 1 = met ,0 = exceeded,t 2 = below
            achievementLevel = rubric.performanceLevel.achievementLevel
            if (achievementLevel == 1 and rubric.numStudents is not None):
                rubricObject['met'] += rubric.numStudents
            elif (achievementLevel == 0 and rubric.numStudents is not None):
                rubricObject['exceeded'] += rubric.numStudents
            elif (rubric.numStudents is not None):
                rubricObject['below'] += rubric.numStudents
            
            rubricExists = False
            for r in rList:
                if (r['perfID'] == rubric.performanceIndicator.id):
                    rubricExists = True
                    r = rubricObject
                    break
                
            if (rubricExists == False):
                rList.append(rubricObject)
                
        outcomeObject['rubricList'] = rList
        #compute the weighted amount for each rubric
        for r in rList:
            numStudents = Decimal(r['met'] + r['exceeded'] + r['below'])
            weight = Decimal(r['weight'] * 100)
            exceeded = Decimal(r['exceeded'] * 1.0)
            met = Decimal(r['met'] * 1.0)
            exceeded = ( exceeded / numStudents ) * weight
            met = ( met / numStudents ) * weight
            
            outcomeObject['exceeded'] += exceeded
            outcomeObject['met'] += met
            outcomeObject['total'] += met + exceeded
        
        outcomeResults.append(outcomeObject)
        
    context = {
        'outcomeList': []
    }
    #group all the outcomes by outcome letter
    sList = studentOutcomes.objects.all()
    objectList = []
    for letter in sList:
        letterObj = {
            'sectionList': [],
            'letter': letter.outcomeLetter,
            'descripton': letter.description
        }
        
        for outcome in outcomeResults:
            if (outcome['letter'] == letterObj['letter']):
                letterObj['sectionList'].append(outcome)
        objectList.append(letterObj)
        
    context['outcomeList'] = objectList
    template = loader.get_template('ABET_DB/graph.html')
    print objectList
    return HttpResponse(template.render(context,request))

def matrix(request):
    nowSem, nowYear = current()
    nowSem = "spring"
    nowYear = "2016"
    #get the student outcomes
    outcomeList = courseOutcomes.objects.all()
    
    #get all sections
    sectionList = sections.objects.all()
    
    #get all performance indicators
    performanceList = performanceIndicators.objects.all()
    
    #get all rubrics
    rubricList = rubrics.objects.all()
    
    sectionsThisSem = sectionList.filter(year = nowYear).filter(semester = nowSem)
    
    outcomeLetters = []
    for outcome in outcomeList:
        outcomeLetters.append(outcome.studentOutcome.outcomeLetter)
    
    context = {
        'sections': [],
        'outcomes': sorted(set(outcomeLetters)),
        'year': nowYear,
        'semester': nowSem
    }
    for section in sectionsThisSem:
        #get all outcomes in this section
        outSec = outcomeList.filter(section = section)
        
        sectionObject = {
            'proffessor': section.professor.fn + " " + section.professor.ln,
            'email': section.professor.netID + "@utk.edu",
            'sectionErrors': [],
            'courseName': section.course.name,
            'message': ""
        }
        
        #loop through each outcome in the section to determine if 
        #outcome is valid
        for outcome in outSec:
            outcomeError = {
                'outcomeLetter': outcome.studentOutcome.outcomeLetter,
                'errorMessage': []
            }
            errorMessage = [] #error message arrary for outcomes
            messageString = ""
            
            perfList = performanceList.filter(outcome = outcome)
            weightCtr = 0       #keeps track of the weight to make sure it equals 1
            studentTotal = 0    #keeps track of num students to make sure consistnet
            if (len(perfList) > 0):
                for perf in perfList:
                    #determine if weight of performance indicators totals to 1
                    weightCtr += perf.weight
                    
                    #get all rubrics in performance indicator
                    rubPerf = rubricList.filter(performanceIndicator = perf)
                    tmpStudent = 0
                    for rubric in rubPerf:
                        if (rubric.numStudents):
                            tmpStudent += rubric.numStudents
                        
                    if (tmpStudent == 0 or tmpStudent < studentTotal):
                        messageString += "Please complete the number of students in rubric: " + perf.name + "%0A"
                        outcomeError['errorMessage'].append("Please complete the number of students in performance indicator: " + perf.name)
                    elif (tmpStudent > studentTotal and studentTotal != 0):
                        messageString += "Please complete the number of students in rubric: " + perf.name + "%0A"
                        outcomeError['errorMessage'].append("Please complete the number of students in performance indicator: " + perf.name)
                    elif (tmpStudent > studentTotal and studentTotal == 0):
                        studentTotal = tmpStudent
                        
                if (weightCtr != 1):
                    messageString += "Please complete entering your performance indicators. The current weight of performance indicators does not equal 1 %0A"
                    outcomeError['errorMessage'].append("Please complete entering your performance indicators. The current weight of performance indicators does not equal 1")
            else: 
                messageString += "Please enter performance indicators for the outcome: " + outcome.studentOutcome.outcomeLetter + "%0A"
                outcomeError['errorMessage'].append("Please enter performance indicators for the outcome: " + outcome.studentOutcome.outcomeLetter)
            
            if (len(outcomeError['errorMessage']) > 0):
                sectionObject['message'] += (outcomeError['outcomeLetter'] + "%0A" + messageString).encode('ascii')
                sectionObject['sectionErrors'].append(outcomeError)
                
            
            
        
        context['sections'].append(sectionObject)
    template = loader.get_template('ABET_DB/matrix.html')
    return HttpResponse(template.render(context, request))
    
# this view returns either an outcome form, or a performance indicator form 
def form(request,what):
    professorNetID = request.session['netid']
    obj = dict()
    
    # retreive all performance levels
    perfLevList = performanceLevels.objects.all()
    
    # retreive the section
    sectionList = sections.objects.filter(professor__netID=professorNetID)     #find courses associated with loged-in professor
    semSem, semYear = tuple(request.GET['semStr'].split('_'))
    sectionsThisSem = sectionList.filter(year=semYear).filter(semester=semSem)
    section = sectionsThisSem.get(course__name=request.GET['course'])
    
    # retreive the outcome
    outcome = courseOutcomes.objects.get(section__pk=section.id, \
                    studentOutcome__outcomeLetter=request.GET['outcome'])



    # begin context for template ( more will be added along the way )
    context = {
        'semStr':request.GET['semStr'],
        'section':section,
        'outcome':outcome,
        'perfLevels':perfLevList,
    }
    
    # if client asks for performance indicator form
    if what == 'pi':
        template = loader.get_template('ABET_DB/pi.html')
        
        # if we are asking for a previously created form
        if request.GET['pi'] != '~':
            
            # retreive the performance indicator
            pi = performanceIndicators.objects.get(outcome__pk=outcome.id, \
                                                    name=request.GET['pi'])
            context['pi'] = pi
            
            # retrieve the rubrics
            rubricList = rubrics.objects.filter(performanceIndicator__pk=pi.id)
            context['rubrics'] = rubricList
    
    # if client asks for the outcome form
    elif what == 'outcome': 
        template = loader.get_template('ABET_DB/outcome.html')
        
        # retreive the outcome data
        odList = outcomeData.objects.filter(outcome__pk=outcome.id)
        context['outcomeData'] = odList
    
    else:
        # url is bad
        raise ABET_Error("form url not 'pi' or 'outcome'")
    
    return HttpResponse(template.render(context,request))

# this view handles data submission from both forms
def submit(request,what):
    
    # retreive the professors netid
    try: professorNetID = request.session['netid']
    except KeyError: 
        raise ABET_Error("Professor's netid not in session data.")
    
    # retrieve sections of the professor
    sectionList = sections.objects.filter(professor__netID=professorNetID)

    if len(sectionList) == 0:
        raise ABET_Error('Section List Empty for Professor')
    
    # retreive the ID of the section
    try: sectionID = request.POST['sectionID']
    except KeyError: 
        raise ABET_Error('sectionID not in POST data')
        
   
    # retreive the course outcome based on section and post data
    section = sectionList.get(pk=sectionID)
    courseOutcomeList = courseOutcomes.objects.filter(section=section)
    courseOutcome = courseOutcomeList.get(studentOutcome__outcomeLetter=request.POST['outcome'])
    
    # retreive performance levels
    perfLevels = performanceLevels.objects.all()
    
    if len(perfLevels) == 0:
        raise ABET_Error('no performanceLevels defined in the database')
    
    # begin data dictionary to return back to client
    data = {
       "professorNetID":professorNetID,
       "course":section.course.name,
       "outcome":courseOutcome.studentOutcome.outcomeLetter,
    }
    
    
    # SUBMITTING PERFORMANCE INDICATOR DATA
    if what == 'pi':
        
        # get a list of performance indicators
        PIList = performanceIndicators.objects.filter(outcome=courseOutcome)
        
        # if the form was for a new performance indicator
        if request.POST['pi'] == '':
            
            # if the name is already taken, return an error state
            # client should prevent this from happening
            if PIList.filter(name=request.POST['newName']).count() != 0:
                return JsonResponse({
                    sucess:False,
                    error:"nameTaken",
                })
            
            # create a new performance indicator
            p = performanceIndicators(name=request.POST['newName'])
            p.outcome = courseOutcome
        
        # if the form was for a prexisting performance indicator
        else:
            # retreive that performance indicator
            p = PIList.get(name=request.POST['pi'])
            
            
            # return an error if the name is already taken
            # client should prevent
            if request.POST['newName'] != request.POST['pi']:
                if PIList.filter(name=request.POST['newName']).count() != 0:
                    return JsonResponse({
                        "success":False,
                        "error":"nameTaken"
                    })
                p.name = request.POST['newName']
                
        # set all the parameters for the performance indicator and save
        p.weight = float(request.POST['weight'])
        if p.weight > 1.0 or p.weight <= 0.0:
            raise ABET_Error('p.weight greater than 1 or less than or equal to 0')
        p.description = request.POST['description']
        p.save()
        
        data['pi'] = p.name
            
        '''
        # populate rubric list if empty
        rubricList = rubrics.objects.filter(performanceIndicator=p)
        if len(rubricList) == 0:
            for pl in perfLevels:
                r = rubrics(performanceLevel=pl,performanceIndicator=p)
                r.save()
            rubricList = rubrics.objects.filter(performanceIndicator=p)
        '''
        # iterate through performance levels, and create corresponding rubrics where nessecary
        for pl in perfLevels:
            a = str(pl.achievementLevel)
            r,cond = rubrics.objects.get_or_create(performanceLevel=pl,performanceIndicator=p)
            
            # record rubric data
            try:
                if request.POST['r_'+a+'_upper']: r.gradeTopBound = int(request.POST['r_'+a+'_upper'])
                if request.POST['r_'+a+'_lower']: r.gradeLowerBound = int(request.POST['r_'+a+'_lower'])
                if request.POST['r_'+a+'_num']:   r.numStudents = int(request.POST['r_'+a+'_num'])
            except ValueError:
                raise ABET_Error('value could not be converted to int')
            
            r.description = request.POST['r_'+a+'_desc']
            r.save()
      
            
    # SUBMIT OUTCOME DATA
    elif what == 'outcome':
        
        '''
        perSectionOutcomeData = outcomeData.objects.filter(outcome=courseOutcome)
        
        if len(perSectionOutcomeData) == 0:         # object doesnt exist, must create object
            for pl in perfLevels:
                a = str(pl.achievementLevel)
                o = outcomeData(outcome=courseOutcome, performanceLevel=pl)
                if request.POST['od_'+a+'_num']: o.numberAchieved = request.POST['od_'+a+'_num']
                o.save()
        
        '''
        
        # iterate through performance levels, and create corresponding outcome data where nessecary
        for pl in perfLevels:
            a = str(pl.achievementLevel)
            o, cond = outcomeData.objects.get_or_create(performanceLevel=pl,outcome=courseOutcome)
        
            if request.POST['od_'+a+'_num']:
                try:
                    o.numberAchieved = int(request.POST['od_'+a+'_num'])
                except ValueError:
                    raise ABET_Error('could not convert value to int')
                
            o.save()
        
        # save the info for the course outcome
        courseOutcome.narrativeSummary = request.POST['narrSum']
        courseOutcome.save()
       
       
    # DELETE A PERFORMANCE INDICATOR
    elif what == 'deletePI':        #delete button pushed
        
        # find the performance indicator
        PIList = performanceIndicators.objects.filter(outcome=courseOutcome)
        
        if len(PIList) == 0:
            raise ABET_Error("Atempting to delete non-existant PI")
        
        p = PIList.get(name=request.POST['pi'])
        p.delete()
      
    else:
        raise ABET_Error("Bad Url in SubmitForm")
    
    return JsonResponse(data)

# this is a debugging view which may be deleted before productions, it populates the database with dummy info 
def populate(request):
    #add performanceLevels
    excede = performanceLevels(achievementLevel=0, description='Exceded Expectations')
    met = performanceLevels(achievementLevel=1, description='Met Expectations')
    didNotMeet = performanceLevels(achievementLevel=2, description='Did Not Meet Expectations')
    excede.save()
    met.save()
    didNotMeet.save()
    
    #add professors
    jkohann = professors(netID='jkohann', fn='Julian', ln='Kohann')
    bvz = professors(netID='bvz', fn='Brad', ln='VZ')
    ahnilica = professors(netID='ahnilica', fn='Andrew', ln='Hnilica')
    stonecoldhughes = professors(netID='stonecoldhughes', fn='Harry', ln='Hughes')
    jkohann.save()
    bvz.save()
    ahnilica.save()
    stonecoldhughes.save()
    
    #add courses
    cs360 = courses(name='cs360', description='Systems Programing')
    cs140 = courses(name='cs140', description='Algorithms 1')
    cs420 = courses(name='cs420', description='Bio Inspired Computing')
    cs401 = courses(name='cs401', description='Sr Design Theory')
    cs402 = courses(name='cs402', description='Sr Design Practicum')
    cs302 = courses(name='cs302', description='Algorithms 2')
    cs102 = courses(name='cs102', description='Intro')
    cs360.save()
    cs140.save()
    cs420.save()
    cs401.save()
    cs402.save()
    cs302.save()
    cs102.save()
    
    #add outcomes
    a = studentOutcomes(outcomeLetter='A', description='description of outcome A')
    b = studentOutcomes(outcomeLetter='B', description='description of outcome B')
    c = studentOutcomes(outcomeLetter='C', description='description of outcome C')
    d = studentOutcomes(outcomeLetter='D', description='description of outcome D')
    e = studentOutcomes(outcomeLetter='E', description='description of outcome E')
    f = studentOutcomes(outcomeLetter='F', description='description of outcome F')
    g = studentOutcomes(outcomeLetter='G', description='description of outcome G')
    h = studentOutcomes(outcomeLetter='H', description='description of outcome H')
    i = studentOutcomes(outcomeLetter='I', description='description of outcome I')
    j = studentOutcomes(outcomeLetter='J', description='description of outcome J')
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
    
    #add sections
    secA = sections(course=cs360, professor=jkohann, year=2016, semester='spring')
    secB = sections(course=cs140, professor=jkohann, year=2016, semester='spring')
    secC = sections(course=cs420, professor=jkohann, year=2016, semester='spring')
    secD = sections(course=cs360, professor=jkohann, year=2015, semester='spring')
    secE = sections(course=cs140, professor=jkohann, year=2015, semester='spring')
    secF = sections(course=cs420, professor=jkohann, year=2015, semester='spring')
    secG = sections(course=cs360, professor=jkohann, year=2015, semester='fall')
    secH = sections(course=cs140, professor=jkohann, year=2015, semester='fall')
    secI = sections(course=cs420, professor=jkohann, year=2015, semester='fall')
    secJ = sections(course=cs360, professor=jkohann, year=2014, semester='spring')
    secA.save()
    secB.save()
    secC.save()
    secD.save()
    secE.save()
    secF.save()
    secG.save()
    secH.save()
    secI.save()
    secJ.save()
    
    #add courseOutcomes
    co1 = courseOutcomes(narrativeSummary='co1', studentOutcome=a, section=secA)
    co2 = courseOutcomes(narrativeSummary='co2', studentOutcome=b, section=secA)
    co3 = courseOutcomes(narrativeSummary='co3', studentOutcome=c, section=secA)
    co4 = courseOutcomes(narrativeSummary='co4', studentOutcome=d, section=secA)
    co5 = courseOutcomes(narrativeSummary='co5', studentOutcome=e, section=secA)
    co6 = courseOutcomes(narrativeSummary='co6', studentOutcome=a, section=secB)
    co7 = courseOutcomes(narrativeSummary='co7', studentOutcome=f, section=secB)
    co8 = courseOutcomes(narrativeSummary='co8', studentOutcome=g, section=secB)
    co9 = courseOutcomes(narrativeSummary='co9', studentOutcome=a, section=secC)
    co1.save()
    co2.save()
    co3.save()
    co4.save()
    co5.save()
    co6.save()
    co7.save()
    co8.save()
    co9.save()
    
    #add performanceIndicators
    one = performanceIndicators(name='one', weight=0.5, description='PI One', outcome=co1)
    two = performanceIndicators(name='two', weight=0.5, description='PI Two', outcome=co1)
    three = performanceIndicators(name='three', weight=0.5, description='PI three', outcome=co2)
    four = performanceIndicators(name='four', weight=0.5, description='PI four', outcome=co2)
    five = performanceIndicators(name='five', weight=0.5, description='PI five', outcome=co2)
    six = performanceIndicators(name='six', weight=0.5, description='PI six', outcome=co3)
    seven = performanceIndicators(name='seven', weight=0.5, description='PI seven', outcome=co4)
    eight = performanceIndicators(name='eight', weight=0.5, description='PI eight', outcome=co4)
    nine = performanceIndicators(name='nine', weight=0.5, description='PI nine', outcome=co4)
    ten = performanceIndicators(name='ten', weight=0.5, description='PI ten', outcome=co6)
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
    
    rubE = rubrics(gradeTopBound=100, gradeLowerBound=90, description='Rubric E', numStudents=50, performanceLevel=excede, performanceIndicator=two)
    rubF = rubrics(gradeTopBound=90, gradeLowerBound=80, description='Rubric F', numStudents=50, performanceLevel=met, performanceIndicator=two)
    rubG = rubrics(gradeTopBound=80, gradeLowerBound=70, description='Rubric G', numStudents=50, performanceLevel=didNotMeet, performanceIndicator=two)
    
    rubI = rubrics(gradeTopBound=100, gradeLowerBound=90, description='Rubric I', numStudents=50, performanceLevel=excede, performanceIndicator=three)
    rubJ = rubrics(gradeTopBound=90, gradeLowerBound=80, description='Rubric J', numStudents=50, performanceLevel=met, performanceIndicator=three)
    rubK = rubrics(gradeTopBound=80, gradeLowerBound=70, description='Rubric K', numStudents=50, performanceLevel=didNotMeet, performanceIndicator=three)
    
    rubM = rubrics(gradeTopBound=100, gradeLowerBound=90, description='rubric m', numStudents=50, performanceLevel=excede, performanceIndicator=four)
    rubN = rubrics(gradeTopBound=90, gradeLowerBound=80, description='Rubric N', numStudents=50, performanceLevel=met, performanceIndicator=four)
    rubO = rubrics(gradeTopBound=80, gradeLowerBound=70, description='Rubric O', numStudents=50, performanceLevel=didNotMeet, performanceIndicator=four)
    rubA.save()
    rubB.save()
    rubC.save()
  
    rubE.save()
    rubF.save()
    rubG.save()
   
    rubI.save()
    rubJ.save()
    rubK.save()
   
    rubM.save()
    rubN.save()
    rubO.save()
    return HttpResponse("Populated Database")

  
def clearDB(request):
    professors.objects.all().delete()
    courses.objects.all().delete()
    studentOutcomes.objects.all().delete()
    performanceLevels.objects.all().delete()
    rubrics.objects.all().delete()
    performanceIndicators.objects.all().delete()
    sections.objects.all().delete()
    courseOutcomes.objects.all().delete()
    outcomeData.objects.all().delete()
    return HttpResponse("Cleared Database")
