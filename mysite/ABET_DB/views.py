from django.shortcuts import render
from django.template import loader

# Create your views here.
from django.http import HttpResponse

def index(request):
    template = loader.get_template('polls/index.html')
    return HttpResponse(template.render())
    
# one view w 3 boxes:
#   StudentOutcomes : outcomeLetters, descripeion
#   PreformanceLevels : aceivementLevel, description
#   Courses : CRNnumber, CourseName, course_description