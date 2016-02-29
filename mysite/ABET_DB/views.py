from django.shortcuts import render
from django.template import loader

# Create your views here.
from ABET_DB.models import studentOutcomes
from django.http import HttpResponse

def index(request):
<<<<<<< HEAD
    return HttpResponse("ABET_DB HOME PAGE")
    
def showData(request):
    outcomeList = studentOutcomes.objects.order_by('outcomeLetter')
    output = ', '.join([q.outcomeLetter for q in outcomeList])
    return HttpResponse(output)
=======
    template = loader.get_template('polls/index.html')
    return HttpResponse(template.render())
    
# one view w 3 boxes:
#   StudentOutcomes : outcomeLetters, descripeion
#   PreformanceLevels : aceivementLevel, description
#   Courses : CRNnumber, CourseName, course_description
>>>>>>> 7f1936debf1170f4d0384b0ebdc90efe6675965c
