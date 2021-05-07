import pexpect
import re

def num_linkages(requirement: str) -> int:
    child = pexpect.spawnu('./parse')
    child.expect('linkparser> ')
    child.sendline(requirement)
    child.expect('linkparser> ', timeout=600)
    res = re.search(r'(?<=Found )\w+', child.before)
    child.sendline('exit')
    return int(res.group(0))

result = []
reqs = []

with open('reqs_new.txt') as f:
    req = f.readline()
    reqs.append(req)
    count = 1
    while req:
        links = num_linkages(req)
        print(f'req {count}, {links} links')
        result.append(links)
        req = f.readline()
        reqs.append(req)
        count += 1
        

with open('tags_new.txt', 'w') as f:
    counter = 0
    for tag in result:
        f.write(f'{tag}~{reqs[counter]}')
        counter +=1
