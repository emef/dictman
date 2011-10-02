from django.db import models

MAX_DISPLAY_LENGTH=30

class Word(models.Model):
    word = models.CharField(max_length=150)
    meaning = models.CharField(max_length=600)
    
    def __unicode__(self):
        return self.word

class Sentence(models.Model):
    text = models.CharField(max_length=600)
    word = models.ForeignKey(Word)

    def __unicode__(self):
        if len(self.text) > MAX_DISPLAY_LENGTH:
            return '%s...' % self.text[:30]
        else:
            return self.text

class Derivative(models.Model):
    text = models.CharField(max_length=600)
    word = models.ForeignKey(Word)

    def __unicode__(self):
        if len(self.text) > MAX_DISPLAY_LENGTH:
            return '%s...' %self.text[:30]
        else:
            return self.text
