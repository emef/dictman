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
    meaning = models.CharField(max_length=600)
    pos = models.CharField(max_length=30, choices=POS_CHOICES)

    def to_dict(self):
        return { 'spelling': self.spelling,
                 'meaning': self.meaning,
                 'pos': self.pos,
                 'derivatives': [d.to_dict() for d in self.derivative_set.all()],
                 'sentences': [s.__unicode__() for s in self.sentence_set.all()],
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
                 'meaning': self.meaning,
                 'pos': self.pos,
                 'sentences': [s.__unicode__() for s in self.sentence_set.all()]
               }
    
    def __unicode__(self):
        return "D[%s]" % self.spelling

# base class for word properties
class BaseProperty(models.Model):
    text = models.CharField(max_length=600)
    word = models.ForeignKey(Word, null=True, blank=True, related_name="%(class)s_set")
    derivative = models.ForeignKey(Derivative, null=True, blank=True, related_name="%(class)s_set")
    
    def __unicode__(self):
        return self.text
    
    class Meta:
        abstract = True

class Sentence(BaseProperty):
    pass 

class Synonym(BaseProperty):
    pass 

class Antonym(BaseProperty):
    pass 


