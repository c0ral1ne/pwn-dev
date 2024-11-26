import sys
sys.path.append('/home/ubuntu/pat/scripts/')
from pwn import *
from pwnfast import Pwn

context.terminal = ['tmux', 'splitw', '-v', '-p', '90']

PROG = ''
libc = ELF('')

### ------------------ EXPLOIT ------------------ ###

r = Pwn(PROG)
