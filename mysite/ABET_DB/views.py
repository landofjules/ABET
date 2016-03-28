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
    
def professorPage(request):
    # after harry figures out security, this wont be needed
    # this should be passed in upon login
    request.session['netid'] = 'jkohann' 
    
    # ANDREW make this filter by professor
    courseList = courses.objects.order_by('courseName')
    
    # run the template
    template = loader.get_template('ABET_DB/prof.html')
    context = {
        'netid':request.session['netid'],
        'courses':courseList,
    }
    return HttpResponse(template.render(context,request))

def pi(request,course,outcome,pi):
    
    
    template = loader.get_template('ABET_DB/pi.html')
    rubricList = rubrics.objects.all() # ANDREW filter this by pi and so forth
    # TODO make these the actual abjects so we can access params in the view
    context = {
        'course':course,
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
    profNetId = request.session['netid'] # ANDREW this is how we will remember the proffessor
    data = []
    
    # if we are asking for the outcomes
    if outcome == '~':
        outcomeList = studentOutcomes.objects.all() # ANDREW make this filter by courseName and profNetId
        for o in outcomeList:
            data.append({'letter':o.outcomeLetter, 'desc':o.description})
        obj = {'courseName':courseName,'data':data}
    else:
        pis = performanceLevels.objects.all() # ANDREW make this filter by profNetId, courseName, and outcome
        for p in pis:
            data.append({'level':p.achievementLevel, 'desc':p.description})
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

