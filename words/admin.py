from words.models import Word, Sentence, Derivative
from django.contrib import admin

class SentenceInline(admin.TabularInline):
    model = Sentence
    extra = 2

class DerivativeInline(admin.TabularInline):
    model = Derivative
    extra = 2

class WordAdmin(admin.ModelAdmin):
    inlines = [SentenceInline, DerivativeInline]
    
admin.site.register(Word, WordAdmin)
