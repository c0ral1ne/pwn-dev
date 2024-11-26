from pwn import *

# WIP - still need to annotate / add documentation

class Pwn():
    def __init__(self, name=None, conn=None, gdb=False, pie_base=0):
        if name:
            self.elf = ELF(name)
            self.sym = self.elf.symbols
            self.plt = self.elf.plt
            self.got = self.elf.got
        
        self.pie_base = pie_base

        self.prog_name = name
        self.prog = None
        if conn:
            host, port = conn.split(' ')
            self.prog = remote(host, int(port))
        elif not gdb:
            self.prog = process(name)

        self._disasm_cache = {}
        self._call_cache = {}
    
    def s(self, data):
        self.prog.send(data)

    def sla(self, after, data):
        self.prog.sendlineafter(after, data)
    
    def sa(self, after, data):
        self.prog.sendafter(after, data)

    def sl(self, data):
        self.prog.sendline(data)
    
    def ru(self, until):
        return self.prog.recvuntil(until)
    
    def rl(self):
        return self.prog.recvline()
    
    def rlc(self, data):
        return self.prog.recvline_contains(data)
    
    def rb(self, n_bytes):
        return self.prog.recv(n_bytes)
    
    def interactive(self):
        self.prog.interactive() 

    def gdb(self, b, c=True):
        script = f'b *{b}'
        if c:
            script += '\nc'
        if self.prog:
            gdb.attach(self.prog, script)
        else:
            self.prog = gdb.debug(self.prog_name, script)

    def get_disasm(self, func_sym):
        if func_sym in self._disasm_cache:
            return self._disasm_cache[func_sym]

        start = self.sym[func_sym]
        n_bytes = 100
        d = self.elf.disasm(start, n_bytes)
        while 'ret' not in d:
            n_bytes += 100
            d = self.elf.disasm(start, n_bytes)
        
        # Cut off everything after ret
        d_pruned = d[:d.index('ret') + 3]

        # Turn into list
        insns = []
        for p in d_pruned.split('\n'):
            addr, _, rest = p.strip().partition(':')
            insns.append((int(addr, 16), rest))
        
        self._disasm_cache[func_sym] = insns
        return insns
    
    def _print_insns(self, insns):
        for i in insns:
            print(i[1])
    
    def ret(self, func_sym):
        insns = self.get_disasm(func_sym)
        addr = insns[-1][0] + self.pie_base
        return hex(addr)

    def call(self, func_sym, sym=None, count=1):
        entry = (func_sym, count, sym)
        if entry in self._call_cache:
            return self._call_cache[entry]

        insns = self.get_disasm(func_sym)
        call_ident = None
        # Filter by sym if specified
        if sym:
            sym_addr = (self.elf.plt[sym] & 0xfffffff0) or self.sym[sym]
            call_ident = f'call   {hex(sym_addr)}'
        
        addr_str = -1
        if call_ident:
            cnt = 0
            for i in insns:
                if call_ident in i[1]:
                    cnt += 1
                    if cnt == count:
                        addr_str = hex(i[0] + self.pie_base)
                        break
        else:
            cnt = 0
            for i in insns:
                if cnt == count and 'call' in i[1]:
                    addr_str = hex(i[0] + self.pie_base)
                    break
                cnt += 1
        
        if addr_str == -1:
            raise Exception('call: could not find specified sym')
        
        self._call_cache[entry] = addr_str
        return addr_str

