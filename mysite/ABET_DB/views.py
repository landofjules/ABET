from django.shortcuts import render

# Create your views here.
from ABET_DB.models import studentOutcomes
from django.http import HttpResponse

def index(request):
    return HttpResponse("ABET_DB HOME PAGE")
    
def showData(request):
    outcomeList = studentOutcomes.objects.order_by('outcomeLetter')
    output = ', '.join([q.outcomeLetter for q in outcomeList])
    return HttpResponse(output)
