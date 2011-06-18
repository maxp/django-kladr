# -*- coding: utf-8 -*-

'''
    mxlab.com: kladr.views
'''

import json
from django.http import HttpResponse

from models import list_level
from models import code_text


def kladr_list( request, code, level ):

    if level not in ['1','2','3','4','5']:
        return HttpResponse( "[]" )

    kl = list_level( code, int(level) )
    res = [ (p[0],p[1]+', '+p[2],) for p in kl ]

    return HttpResponse( json.dumps(res), mimetype='application/json' )
#--

def kladr_text( request, code ):
    t = code_text( code )
    
    return HttpResponse( json.dumps(t), mimetype='application/json' )
#--

#.
