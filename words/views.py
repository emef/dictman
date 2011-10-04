from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from words.models import Word

import simplejson as json

def word_list(request):
    return TemplateResponse(request, 'words/word_list.djhtml', {})

def get_word_ids(request):
    ws = [{'spelling': w.spelling,
           'id': w.id} 
          for w in Word.objects.all()]
    return HttpResponse(json.dumps(ws))
    
def get_word(request, id):
    word = get_object_or_404(Word, id=id)
    return HttpResponse(word.to_json())
