from words.models import Word, Derivative, Meaning, Synonym, Antonym
from django.contrib import admin

class MeaningInline(admin.TabularInline):
    model = Meaning
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
    inlines = [MeaningInline,
               DerivativeInline, 
               SynonymInline,
               AntonymInline]

class DerivativeAdmin(admin.ModelAdmin):
    inlines = [MeaningInline]
               
    
admin.site.register(Word, WordAdmin)
admin.site.register(Derivative, DerivativeAdmin)
