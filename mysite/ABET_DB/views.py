from django.shortcuts import render
from django.template import loader

# Create your views here.
from ABET_DB.models import studentOutcomes
from django.http import HttpResponse

def index(request):
    template = loader.get_template('ABET_DB/index.html')
    return HttpResponse(template.render())
    
def showData(request):
    outcomeList = studentOutcomes.objects.order_by('outcomeLetter')
    output = ', '.join([q.outcomeLetter for q in outcomeList])
    return HttpResponse(output)
    
# one view w 3 boxes:
#   StudentOutcomes : outcomeLetters, descripeion
#   PreformanceLevels : aceivementLevel, description
#   Courses : CRNnumber, CourseName, course_description
