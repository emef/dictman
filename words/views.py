from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.template import RequestContext
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from words.models import Word, Derivative, Meaning, Synonym, Antonym
from words.xml import to_xml

import simplejson as json

def superuser_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("false")

    return _wrapped_view

def word_list(request):
    c = RequestContext(request, {'mode': 'default'})
    return TemplateResponse(request, 'words/word_list.html', c)

def favorites(request):
    c = RequestContext(request, {'mode': 'favorites'} )
    return TemplateResponse(request, 'words/word_list.html', c)

@superuser_required
def xml(request, words=None):
    words = Word.objects.select_related(depth=3).all()
    response = HttpResponse(mimetype='text/xml')
    response['Content-Disposition'] = 'attachment; filename=dict.xml'
    response.write(to_xml(words))
    return response

def get_word_ids(request):
    def get_or_default(lst, i, default):
        try:
            return lst[i].text
        except IndexError:
            return default
        
    ws = [{'spelling': w.spelling,
           'meaning': get_or_default(list(w.meaning_set.all()), 0, 'text'),
           'id': w.id} 
          for w in Word.objects.select_related(depth=1).all()]
    return HttpResponse(json.dumps(ws))

@login_required
def get_favorites_ids(request):
    def get_or_default(lst, i, default):
        try:
            return lst[i].text
        except IndexError:
            return default

    ws = [{'spelling': w.spelling,
           'meaning': get_or_default(list(w.meaning_set.all()), 0, 'text'),
           'id': w.id} 
          for w in request.user.userprofile.favorites.all()]

    return HttpResponse(json.dumps(ws))
          

    
def get_word(request, id):
    word = get_object_or_404(Word, id=id)
    return HttpResponse(word.to_json())

@superuser_required
def add_word(request):
    try:
        w_obj = json.loads(request.POST['w_obj'])
        # first add word object
        w = Word(spelling = w_obj['spelling'], 
                 level = w_obj['level'])
        w.save()
        #add meaning
        for m in w_obj['meanings']:
            w.meaning_set.create(text = m['text'],
                                 pos = m['pos'],
                                 example = m['example'])
        #add derivatives
        for d in w_obj['derivatives']:
            deriv = w.derivative_set.create(spelling = d['spelling'])
            for m in d['meanings']:
                deriv.meaning_set.create(text = m['text'],
                                         pos = m['pos'],
                                         example = m['example'])

        #now synonyms
        [w.synonym_set.create(text=syn) for syn in w_obj['synonyms']]

        #antonyms
        [w.antonym_set.create(text=syn) for syn in w_obj['antonyms']]
        
        return HttpResponse(json.dumps({'spelling': w.spelling, 'id': w.id}))
    except json.decoder.JSONDecodeError:
        return HttpResponse("false")

@superuser_required
def edit_word(request):
    try:
        w_obj = json.loads(request.POST['w_obj'])
        w = Word.objects.select_related().get(id=w_obj['id']);
        w.spelling = w_obj['spelling']
        w.level = w_obj['level']

        #remove old meanings
        w.meaning_set.all().delete()

        #add meanings
        for m in w_obj['meanings']:
            w.meaning_set.create(text = m['text'],
                                 pos = m['pos'],
                                 example = m['example'])
            
        #remove old derivatives
        w.derivative_set.all().delete()

        #add new derivatives
        for d in w_obj['derivatives']:
            deriv = w.derivative_set.create(spelling = d['spelling'])
                                            
            #add meanings
            for m in d['meanings']:
                deriv.meaning_set.create(text = m['text'],
                                         pos = m['pos'],
                                         example = m['example'])

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

@superuser_required
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
    
@login_required
def add_to_fav(request):
    try:
        id = json.loads(request.POST['id'])
        word = get_object_or_404(Word, id=id)
        request.user.userprofile.favorites.add(word)
        request.user.userprofile.save()
        
        return HttpResponse("true")
    except json.decoder.JSONDecodeError:
        return HttpResponse("false")

@login_required
def remove_fav(request):
    try:
        id = json.loads(request.POST['id'])
        word = get_object_or_404(Word, id=id)
        request.user.userprofile.favorites.remove(word)
        request.user.userprofile.save()
        
        return HttpResponse("true")
    except json.decoder.JSONDecodeError:
        return HttpResponse("false")

