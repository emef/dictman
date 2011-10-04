from words.models import Word, Derivative, Sentence, Synonym, Antonym
from django.contrib import admin

class SentenceInline(admin.TabularInline):
    model = Sentence
    extra = 1
    
class SynonymInline(admin.TabularInline):
    model = Synonym
    extra = 1

class AntonymInline(admin.TabularInline):
    model = Antonym
    extra = 1

class DerivativeInline(admin.TabularInline):
    model = Derivative
    extra = 1

class WordAdmin(admin.ModelAdmin):
    inlines = [DerivativeInline, 
               SentenceInline, 
               SynonymInline,
               AntonymInline]

class DerivativeAdmin(admin.ModelAdmin):
    inlines = [SentenceInline]
               
    
admin.site.register(Word, WordAdmin)
admin.site.register(Derivative, DerivativeAdmin)
