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
    
class Word(models.Model):
    spelling = models.CharField(max_length=150)

    pos = models.CharField(max_length=30, choices=POS_CHOICES)

    def to_dict(self):
        return { 'spelling': self.spelling,
                 'meanings': [m.to_dict() for m in self.meaning_set.all()],
                 'pos': self.pos,
                 'derivatives': [d.to_dict() for d in self.derivative_set.all()],
                 'synonyms': [s.__unicode__() for s in self.synonym_set.all()],
                 'antonyms': [a.__unicode__() for a in self.antonym_set.all()]
               } 
    
    def to_json(self):
        return json.dumps(self.to_dict())
    
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


