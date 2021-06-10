import xmltodict
import re

def xml_file_to_dict(path: str) -> dict:
    with open(path) as f:
        doc = xmltodict.parse(f.read())
    return doc


def interpret_dict(content: dict, find: list) -> list:
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

    read_json(content, find)

    return results


def create_reqs(raw_reqs: list, items_are_reqs=False) -> list:
    stack = []
    reqs = []

    for tag, text in raw_reqs:

        text = re.sub('	+', '', text) # remove tabs

        text = text.replace('\n', '').replace(';', '').replace('<', '').replace('>', '') # remove some chars
        
        text = text.replace('“', '"').replace('”', '"').replace(' — ', ', ').replace('’', "'").replace('-', ' ').replace('/', " or ") # replace some chars with alternatives

        text = text.replace('i.e.', 'that is').replace('e.g.', 'for example') # replace latin abbreviations

        text = re.sub(' +', ' ', text) # remove extra spaces

        if tag == '__list_item__':
            if items_are_reqs:
                reqs.append(text)
            else:
                stack.append(text)
        elif tag == '__#text__':
            if items_are_reqs:
                pass
            else:
                reqs.append(text + ' ' + ', '.join(stack))
                stack = []
        elif tag == '__text_body__':
            reqs.append(text)
            stack = []

    return reqs


def break_lines(reqs: list) -> list:
    result = []
    for req in reqs:
        new = req.replace('. ', '.\n')
        result.append(new)

    return result


def write_req_file(name: str, reqs: list):    
    with open(name, 'w') as f:
        for req in reqs:
            f.write(f'{req}\n')


if __name__ == '__main__':

    reqs = []

    # doc = xml_file_to_dict('datos/0000 - cctns.xml')
    # results = interpret_dict(doc, ['text_body', '#text', 'title'])
    # reqs = create_reqs(results)
    # reqs = break_lines(reqs)

    # doc = xml_file_to_dict('datos/0000 - gamma j.xml')
    # results = interpret_dict(doc, ['text_body', '#text', 'title'])
    # reqs_1 = create_reqs(results, items_are_reqs=True)
    # reqs += break_lines(reqs_1)

    # doc = xml_file_to_dict('datos/1995 - gemini.xml')
    # results = interpret_dict(doc, ['text_body', '#text', 'title'])
    # reqs_1 = create_reqs(results, items_are_reqs=True)
    # reqs += break_lines(reqs_1)

    # doc = xml_file_to_dict('datos/1998 - themas.xml')
    # results = interpret_dict(doc, ['text_body', '#text', 'title'])
    # reqs_1 = create_reqs(results, items_are_reqs=True)
    # reqs += break_lines(reqs_1)

    # doc = xml_file_to_dict('datos/1999 - dii.xml')
    # results = interpret_dict(doc, ['text_body', '#text', 'title'])
    # reqs_1 = create_reqs(results, items_are_reqs=True)
    # reqs += break_lines(reqs_1)

    # doc = xml_file_to_dict('datos/1999 - tcs.xml')
    # results = interpret_dict(doc, ['text_body', '#text', 'title'])
    # reqs_1 = create_reqs(results, items_are_reqs=False)
    # reqs += break_lines(reqs_1)

    # doc = xml_file_to_dict('datos/2003 - qheadache.xml')
    # results = interpret_dict(doc, ['text_body', '#text', 'title'])
    # reqs_1 = create_reqs(results, items_are_reqs=False)
    # reqs += break_lines(reqs_1)

    # doc = xml_file_to_dict('datos/2005 - microcare.xml')
    # results = interpret_dict(doc, ['text_body', '#text', 'title'])
    # reqs_1 = create_reqs(results, items_are_reqs=True)
    # reqs += break_lines(reqs_1)

    # doc = xml_file_to_dict('datos/2005 - phin.xml')
    # results = interpret_dict(doc, ['text_body', '#text', 'title'])
    # reqs_1 = create_reqs(results, items_are_reqs=True)
    # reqs += break_lines(reqs_1)

    # doc = xml_file_to_dict('datos/2007 - get real 0.2.xml')
    # results = interpret_dict(doc, ['text_body', '#text', 'title'])
    # reqs_1 = create_reqs(results, items_are_reqs=False)
    # reqs += break_lines(reqs_1)

    doc = xml_file_to_dict('datos/2007-ertms.xml')
    results = interpret_dict(doc, ['text_body', '#text', 'title'])
    reqs_1 = create_reqs(results, items_are_reqs=False)
    reqs += break_lines(reqs_1)

    write_req_file('reqs_new.txt', reqs)
