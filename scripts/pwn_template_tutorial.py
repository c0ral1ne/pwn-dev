from pwn import *

context.terminal = ['tmux', 'splitw', '-v', '-p', '90']

PROG = ''
elf = ELF(PROG)
libc = ELF('')

### ------------------ EXPLOIT ------------------ ###

r = process(PROG)
