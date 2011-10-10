from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.template import RequestContext
from words.models import Word, Derivative, Meaning, Synonym, Antonym
from words.xml import to_xml

import simplejson as json

def word_list(request):
    c = RequestContext(request, {})
    return TemplateResponse(request, 'words/word_list.djhtml', c)

def xml(request, words=None):
    words = Word.objects.select_related().all()
    response = HttpResponse(mimetype='text/xml')
    response['Content-Disposition'] = 'attachment; filename=dict.xml'
    response.write(to_xml(words))
    return response

def get_word_ids(request):
    ws = [{'spelling': w.spelling,
           'id': w.id} 
          for w in Word.objects.all()]
    return HttpResponse(json.dumps(ws))
    
def get_word(request, id):
    word = get_object_or_404(Word, id=id)
    return HttpResponse(word.to_json())

def add_word(request):
    try:
        w_obj = json.loads(request.POST['w_obj'])
        # first add word object
        w = Word(spelling = w_obj['spelling'], 
                 pos = w_obj['pos'], 
                 level = w_obj['level'])
        w.save()
        #add meaning
        w.meaning_set.create(text = w_obj['meanings'][0]['text'], 
                             example = w_obj['meanings'][0]['example'])
        #add derivatives
        for d in w_obj['derivatives']:
            deriv = w.derivative_set.create(spelling = d['spelling'], 
                                              pos = d['pos'])
            deriv.meaning_set.create(text = d['meanings'][0]['text'],
                                     example = d['meanings'][0]['example'])

        #now synonyms
        [w.synonym_set.create(text=syn) for syn in w_obj['synonyms']]

        #antonyms
        [w.antonym_set.create(text=syn) for syn in w_obj['antonyms']]
        
        return HttpResponse(json.dumps({'spelling': w.spelling, 'id': w.id}))
    except json.decoder.JSONDecodeError:
        return HttpResponse("false")

def edit_word(request):
    try:
        w_obj = json.loads(request.POST['w_obj'])
        w = Word.objects.select_related().get(id=w_obj['id']);
        w.spelling = w_obj['spelling']
        w.pos = w_obj['pos']
        w.level = w_obj['level']

        m = w.meaning_set.all()[0]
        m.text = w_obj['meanings'][0]['text']
        m.example = w_obj['meanings'][0]['example']
        m.save()

        #remove old derivatives
        w.derivative_set.all().delete()

        #add new derivatives
        for d in w_obj['derivatives']:
            deriv = w.derivative_set.create(spelling = d['spelling'], 
                                              pos = d['pos'])
            deriv.meaning_set.create(text = d['meanings'][0]['text'],
                                     example = d['meanings'][0]['example'])

        #now synonyms
        w.synonym_set.all().delete()
        [w.synonym_set.create(text=syn) for syn in w_obj['synonyms']]

        #antonyms
        w.antonym_set.all().delete()
        [w.antonym_set.create(text=syn) for syn in w_obj['antonyms']]

        w.save()
        return HttpResponse(json.dumps({'spelling': w.spelling, 'id': w.id}))
    except json.decoder.JSONDecodeError:
        return HttpResponse("false")

def delete_word(request):
    try:
        id = json.loads(request.POST['id'])
        w = Word.objects.select_related().get(id=id)
        w.meaning_set.all().delete()
        w.synonym_set.all().delete()
        w.antonym_set.all().delete()
        for d in w.derivative_set.all():
            d.meaning_set.all().delete()
            d.delete()
        w.delete()
        
        return HttpResponse("true")
    except json.decoder.JSONDecodeError:
        return HttpResponse("false")
    
