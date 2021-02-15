import xmltodict
import re

with open('0000 - cctns.xml') as fd:
    doc = xmltodict.parse(fd.read())

results = []

def read_json(content, find):
    if isinstance(content, dict):
        for key in content.keys():
            if key in find:
                if isinstance(content[key], str):
                    results.append((f'__{key}__', content[key]))
            read_json(content[key], find)
    elif isinstance(content, list):
        for elem in content:
            if isinstance(elem, str):
                results.append(('__list_item__', elem))
            else:
                read_json(elem, find)   
    else:
        pass


read_json(doc, ['text_body', '#text', 'title'])


def create_reqs(raw_reqs):
    stack = []
    reqs = []

    for tag, text in raw_reqs:

        text = text.replace('\n', '').replace(';', '').replace('<', '').replace('>', '') # remove some chars
        
        text = text.replace('“', '"').replace('”', '"').replace(' — ', ', ').replace('’', "'").replace('-', ' ').replace('/', " or ") # replace some chars with alternatives

        text = text.replace('i.e.', 'that is').replace('e.g.', 'for example') # replace latin abbreviations

        text = re.sub(' +', ' ', text) # remove extra spaces

        if tag == '__list_item__':
            stack.append(text)
        elif tag == '__#text__':
            reqs.append(text + ' ' + ', '.join(stack))
            stack = []
        elif tag == '__text_body__':
            reqs.append(text)
            stack = []

    return reqs


reqs = create_reqs(results)

print(reqs)