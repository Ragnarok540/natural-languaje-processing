import spacy
from spacy.util import minibatch
from spacy.training import Example
import pandas as pd
import sys
import random

def add_labels(df):
    bins = [0, 10, 100, sys.maxsize]
    labels = ['low', 'medium', 'high']
    group = pd.cut(df['links'], bins=bins, labels=labels)
    df['label'] = group
    return df

# Load data
data = pd.read_csv('tags.txt', sep='~', header=None)

data.columns = ['links', 'req']

add_labels(data)

#texts = data[-6:]

#data = data[0:-6]

train_texts = data['req'].values
train_labels = [{'cats': {'low': label == 'low',
                          'medium': label == 'medium',
                          'high': label == 'high'}} for label in data['label']]

train_data = list(zip(train_texts, train_labels))



# Create an empty model
nlp = spacy.blank("en")

# Add the TextCategorizer to the empty model
textcat = nlp.add_pipe("textcat")

textcat.add_label("low")
textcat.add_label("medium")
textcat.add_label("high")

examples = []

for text, annots in train_data:
    examples.append(Example.from_dict(nlp.make_doc(text), annots))
    nlp.initialize(lambda: examples)

random.seed(1)
spacy.util.fix_random_seed(1)
optimizer = nlp.begin_training()

losses = {}
for epoch in range(10):
    random.shuffle(examples)
    # Create the batch generator with batch size = 8
    batches = minibatch(examples, size=8)
    # Iterate through minibatches
    for batch in batches:
        # Update the model with a new batch
        nlp.update(batch, sgd=optimizer, losses=losses)
    print(losses)

texts = [ 'Failure conditions should not cascade', 'The system should monitor the rate of warning messages since an increase might indicate that some tuning or maintenance is appropriate', ]

docs = [nlp.tokenizer(text) for text in texts]
    
# Use textcat to get the scores for each doc
textcat = nlp.get_pipe('textcat')
scores, _ = textcat.predict(docs)

print(scores)

predicted_labels = scores.argmax(axis=0)


print(textcat.labels[predicted_labels])
#print([textcat.labels[label] for label in predicted_labels])
