#from gensim.models import Word2Vec

#sentences = [["cat", "say", "meow"], ["dog", "say", "woof"]]

#model = Word2Vec(min_count=1)

#model.build_vocab(sentences)  # prepare the model vocabulary

#model.train(sentences, total_examples=model.corpus_count, epochs=model.epochs)  # train word vectors

#print(model.wv['say'])

import spacy

nlp = spacy.load("en_core_web_lg")  # make sure to use larger package!
doc1 = nlp("cat")
doc2 = nlp("feline")

# Similarity of two documents
print(doc1, "<->", doc2, doc1.similarity(doc2))
print(doc1.vector)
