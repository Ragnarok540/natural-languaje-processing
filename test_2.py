import pexpect
import sys

child = pexpect.spawnu('./parse')

child.expect('linkparser> ')
child.sendline('mary saw a dog')
child.expect('linkparser> ')
print(child.before)
child.sendline('exit')
