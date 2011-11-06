from myxml.dom.minidom import Document
from words.models import Word

def to_xml(words):
    doc = Document()
    dictionary = doc.createElement('d:dictionary')
    dictionary.setAttribute('xmlns', 'http://www.w3.org/1999/xhtml')
    dictionary.setAttribute('xmlns:d', 'http://www.apple.com/DTDs/DictionaryService-1.0.rng')
    doc.appendChild(dictionary)

    for w in words:
        dictionary.appendChild(w.to_xml(doc))

    return doc.toprettyxml()
    
    
