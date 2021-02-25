import benepar
#benepar.download('benepar_en3')

import spacy

nlp = spacy.load('en_core_web_md')
if spacy.__version__.startswith('2'):
    nlp.add_pipe(benepar.BeneparComponent("benepar_en3"))
else:
    nlp.add_pipe("benepar", config={"model": "benepar_en3"})
doc = nlp("The System must be able to retrieve and display within 20 seconds the case which has not been accessed within the previous 2 months, regardless of storage capacity or number of cases in the system.")
sent = list(doc.sents)[0]
print(sent._.parse_string)

import nltk

t = nltk.Tree.fromstring(sent._.parse_string)

t.draw()
