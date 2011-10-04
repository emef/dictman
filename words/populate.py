from words.models import *
from random import random
from math import floor, ceil

DICT_FILE='/usr/share/dict/words'

def get_random_words(n):
    ws = []
    with open(DICT_FILE) as file:
        count = 0
        for line in file:
            count = count + 1
        file.seek(0)
        for x in xrange(n):
            ln = int(floor(random() * count))
            for y in xrange(ln):
                file.readline()
            ws.append(file.readline().replace('\n', ''))
            file.seek(0)
        return ws

def populate(n):
    rnd_words = get_random_words(n)
        
    def rndwords():
        num = int(ceil(random() * 5))
        a = []
        for x in range(num):
            a.append(rnd_words[int(floor(random() * len(rnd_words)))])
        return a

    for sp in rnd_words:
        w = Word(spelling=sp, pos='v')
        w.level = int(ceil(random() * 5))
        w.save()
        w.meaning_set.add(Meaning(text='generic meaning for %s' % sp, 
                                  example='generic example for %s' % sp))
        for syn in rndwords():
            w.synonym_set.add(Synonym(text=syn))
        for ant in rndwords():
            w.antonym_set.add(Antonym(text=ant))

        w.save()
        
        d = Derivative(parent=w, spelling='%sed' % sp, pos='v')
        d.save()
        d.meaning_set.add(Meaning(text='derivative generic meaning for %s' % d.spelling,
                                  example='derivative example for %s' % d.spelling))
        d.save()
        
        
    
        
        
    
    
