import spacy 
nlp=spacy.load('en_core_web_md')
ner_labels=nlp.get_pipe('ner')
print(ner_labels)