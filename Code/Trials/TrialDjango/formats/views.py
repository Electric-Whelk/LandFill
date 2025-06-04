from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

import sys
sys.path.insert(1, '../TrialDatabase/')
from Format import Format
from Configure_DB import engine
from Configure_DB import session as dbsesh

# Create your views here.
def formats(request):
    all_formats = dbsesh.query(Format).all()
    template = loader.get_template('myfirst.html')
    context = {
        'all_formats': all_formats
    }
    return HttpResponse(template.render(context, request))
