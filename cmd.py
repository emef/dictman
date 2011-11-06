#!/usr/bin/env python
from django.core.management import setup_environ

import settings

setup_environ(settings)

from words.models import Word, Meaning, Derivative, POS_CHOICES, LEVEL_CHOICES

DEBUG = False

# ADDING WORD
#######################################################################
def get_pos(prompt):
    pos_options = [pos[0] for pos in POS_CHOICES]
    while True:
        resp = raw_input(prompt)
        if resp in pos_options:
            return resp
        print 'please enter one of: %s' % ', '.join(pos_options)
        
def get_level(prompt):
    level_options = [str(l[0]) for l in LEVEL_CHOICES]
    while True:
        try:
            resp = int(raw_input(prompt))
            return resp
        except ValueError:
            print 'please enter one of: %s' % ', '.join(level_options)

def get_bool(prompt):
    bool_options = ['y', 'n',]
    while True:
        resp = raw_input(prompt)
        if resp == 'y':
            return True
        elif resp == 'n':
            return False
        print 'please enter one of: %s' % ', '.join(bool_options)

def get_meaning(pos_prompt, text_prompt, example_prompt):
    m = Meaning()
    m.pos = get_pos(pos_prompt)
    m.text = raw_input(text_prompt)
    m.example = raw_input(example_prompt)
    return m

def print_meaning(pos, meaning, example, prefix):
    print '%s%s\n%s%s\n%s%s\n' % (prefix, pos, prefix, meaning, prefix, example)

def add_word():
    w = Word()
    w.spelling = raw_input('::: word spelling ::: >> ')
    w.level = get_level('::: word level ::: >> ')
    
    #get meanings
    meanings = []
    def meaning_prompt(lst, spelling):
        if len(lst) == 0:
            return 'add a meaning to %s? >> ' % spelling
        else:
            return 'add another meaning to %s? >> ' % spelling
        
    while(get_bool(meaning_prompt(meanings, w.spelling))):
        meanings.append(get_meaning('::: POS ::: >> ', 
                                    '::: meaning ::: >> ', 
                                    '::: example ::: >> '))

    #get derivatives
    derivatives = []
    def derivative_prompt():
        if len(derivatives) == 0:
            return 'add a derivative to %s >> ' % w.spelling
        else:
            return 'add another derivative to %s >> ' % w.spelling

    while(get_bool(derivative_prompt())):
        d = Derivative()
        d.spelling = raw_input('::: derivative spelling ::: >> ')
        
        d_meanings = []
        while(get_bool(meaning_prompt(d_meanings, d.spelling))):
            d_meanings.append(get_meaning('::: POS ::: >> ',
                                          '::: meaning ::: >> ', 
                                          '::: example ::: >> '))

        derivatives.append((d, d_meanings))

    # confirm adding word
    print ''
    print '%s:\nlevel %d\n' % (w.spelling, w.level)
    for m in meanings:
        print_meaning(m.pos, m.text, m.example, '    ')

    for d, ms in derivatives:
        prefix = '    '
        print '%s%s:\n' % (prefix, d.spelling)
        for m in ms:
            print_meaning(m.pos, m.text, m.example, 2*prefix)

    if get_bool('add this word to the database? >> '):
        w.save()
        for m in meanings:
            w.meaning_set.add(m)
        for d, ms in derivatives:
            d.parent = w
            d.save()
            for m in ms:
                d.meaning_set.add(m)
            w.derivative_set.add(d)
        print '%s added to database successfuly\n' % w.spelling
    
    
# ADDING WORD
#######################################################################
def delete_word():
    spelling = raw_input('which word should I delete? ')
    try:
        w = Word.objects.get(spelling=spelling)
        if get_bool('really delete word %s? ' % w.spelling):
            w.delete()
            print 'successfully deleted %s' % w.spelling
        else:
            print 'did not delete %s' % w.spelling
    except Word.DoesNotExist:
        print 'could not find word in database'
    if get_bool('delete another word? '):
        delete_word()
    
    
# MAIN PROGRAM
#######################################################################
def main():
    options = [
        ('add a word', 'add', add_word),
        ('delete a word', 'delete', delete_word),
        ('quit the program', 'quit', exit),
    ]
    while(1):
        for prompt, cmd, _ in options:
            print '%s -- %s' % (cmd, prompt)
            
        resp = raw_input('>> ')
        
        if DEBUG and resp == 'quit':
            break
        
        handled = False
        for _, cmd, fn in options:
            if resp == cmd:
                fn()
                handled = True
                break
        if not handled:
            print 'invalid command'
    
if __name__ == "__main__":
    main()
