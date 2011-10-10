from django.db import models

import simplejson as json

MAX_DISPLAY_LENGTH=30
POS_CHOICES = (
    ('v', 'verb',),
    ('n', 'noun',),
    ('P', 'pronoun',),
    ('adj', 'adjective',),
    ('adv', 'adverb',),
)
LEVEL_CHOICES = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
)
    
class Word(models.Model):
    spelling = models.CharField(max_length=150)
    level = models.IntegerField(choices=LEVEL_CHOICES, blank=True)
    pos = models.CharField(max_length=30, choices=POS_CHOICES)
    
    def to_dict(self):
        return { 'spelling': self.spelling,
                 'level': self.level,
                 'meanings': [m.to_dict() for m in self.meaning_set.all()],
                 'pos': self.pos,
                 'derivatives': [d.to_dict() for d in self.derivative_set.all()],
                 'synonyms': [s.__unicode__() for s in self.synonym_set.all()],
                 'antonyms': [a.__unicode__() for a in self.antonym_set.all()]
               } 
    
    def to_json(self):
        return json.dumps(self.to_dict())

    def pos_str(self):
        for key,val in POS_CHOICES:
            if self.pos == key:
                return val

    def to_xml(self, doc):
        entry = doc.createElement('d:entry')
        entry.setAttribute('id', self.spelling)
        entry.setAttribute('d:title', self.spelling)
        
        def make_index(spelling):
            emt = doc.createElement('d:index')
            emt.setAttribute('d:value', spelling)
            return emt

        def tag(tagname, text=None):
            emt = doc.createElement(tagname)
            if text is not None:
                tn = doc.createTextNode(text)
                emt.appendChild(tn)
            return emt
        
        def div(text=None):
            return tag('div', text)

        #make entries
        entry.appendChild(make_index(self.spelling))
        for d in self.derivative_set.all():
            entry.appendChild(make_index(d.spelling))
        for syn in self.synonym_set.all():
            entry.appendChild(make_index(syn.text))
        for ant in self.antonym_set.all():
            entry.appendChild(make_index(ant.text))

        #level
        entry.appendChild(div(str(self.level)))

        def make_word(obj):
            d = div()
            d.appendChild(tag('h1', obj.spelling))
            entry.appendChild(d)

            #POS
            if hasattr(obj, 'pos'):
                entry.appendChild(div('noun'))
                #entry.appendChild(div(obj.pos_str()))

            #meanings
            m_div = div()
            ol = tag('ol')
            for m in obj.meaning_set.all():
                li = tag('li', '%s :' % m.text)
                span = tag('span')
                ital = tag('i')
                ital.appendChild(doc.createTextNode(m.example))
                span.appendChild(ital)
                li.appendChild(span)
                ol.appendChild(li)

            m_div.appendChild(ol)
            d.appendChild(m_div)
            
            return d
            
        #main word
        entry.appendChild(make_word(self))
        for d in self.derivative_set.all():
            entry.appendChild(make_word(d))

        #synonyms
        h = tag('h3', 'SYNONYMS')
        entry.appendChild(h)
        span = tag('span', ', '.join([s.text for s in self.synonym_set.all()]))
        entry.appendChild(span)

        #antonyms
        h = tag('h3', 'ANTONYMS')
        entry.appendChild(h)
        span = tag('span', ', '.join([s.text for s in self.antonym_set.all()]))
        entry.appendChild(span)
        
        return entry
    
    def __unicode__(self):
        return self.spelling

class Derivative(models.Model):
    parent = models.ForeignKey(Word)
    spelling = models.CharField(max_length=150)
    meaning = models.CharField(max_length=600)
    pos = models.CharField(max_length=30, choices=POS_CHOICES)
    
    def to_dict(self):
        return { 'spelling': self.spelling,
                 'meanings': [m.to_dict() for m in self.meaning_set.all()],
                 'pos': self.pos,
                 }  
                 
    def __unicode__(self):
        return "D[%s]" % self.spelling

# base class for word properties
class BaseProperty(models.Model):
    word = models.ForeignKey(Word, null=True, blank=True, related_name="%(class)s_set")
    derivative = models.ForeignKey(Derivative, null=True, blank=True, related_name="%(class)s_set")
    text = models.CharField(max_length=600)
    
    def __unicode__(self):
        if len(self.text) > 30:
            return '%s...' % self.text[:30]
        else:
            return self.text
        
    class Meta:
        abstract = True

class Meaning(BaseProperty):
    example = models.CharField(max_length=600, blank=True)

    def to_dict(self):
        return { 'text': self.text,
                 'example': self.example
               }
    
class Synonym(BaseProperty):
    pass 

class Antonym(BaseProperty):
    pass 


