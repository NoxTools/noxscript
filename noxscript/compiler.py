from .ast import *
from .passes import *
from .parser import gen_ast

import struct

DUMMY = intern('DUMMY')
GLOBAL = intern('GLOBAL')
MAGIC = 'NOXSCRIPT3.0'
UOPS_MAP = {
    (INT, '!'): 0x3e,
    (INT, '~'): 0x3f,
    (INT, '-'): 0x40,
    (FLOAT, '-'): 0x41,
}
OPS_MAP = {
    (INT, '+'): 0x07,
    (FLOAT, '+'): 0x08,
    (INT, '-'): 0x09,
    (FLOAT, '-'): 0x0a,
    (INT, '*'): 0x0b,
    (FLOAT, '*'): 0x0c,
    (INT, '/'): 0x0d,
    (FLOAT, '/'): 0x0e,
    (INT, '%'): 0x0f,
    (INT, '&'): 0x10,
    (INT, '|'): 0x11,
    (INT, '^'): 0x12,
    (INT, '='): 0x16,
    (OBJECT, '='): 0x16,
    (FLOAT, '='): 0x17,
    (STRING, '='): 0x18,
    (INT, '*='): 0x19,
    (FLOAT, '*='): 0x1a,
    (INT, '/='): 0x1b,
    (FLOAT, '/='): 0x1c,
    (INT, '+='): 0x1d,
    (FLOAT, '+='): 0x1e,
    (STRING, '+='): 0x1f,
    (INT, '-='): 0x20,
    (FLOAT, '-='): 0x21,
    (INT, '%='): 0x22,
    (INT, '=='): 0x23,
    (OBJECT, '=='): 0x23,
    (FLOAT, '=='): 0x24,
    (STRING, '=='): 0x25,
    (INT, '<<'): 0x26,
    (INT, '>>'): 0x27,
    (INT, '<'): 0x28,
    (FLOAT, '<'): 0x29,
    (STRING, '<'): 0x2a,
    (INT, '>'): 0x2b,
    (FLOAT, '>'): 0x2c,
    (STRING, '>'): 0x2d,
    (INT, '<='): 0x2e,
    (FLOAT, '<='): 0x2f,
    (STRING, '<='): 0x30,
    (INT, '>='): 0x31,
    (FLOAT, '>='): 0x32,
    (STRING, '>='): 0x33,
    (INT, '!='): 0x34,
    (OBJECT, '!='): 0x34,
    (FLOAT, '!='): 0x35,
    (STRING, '!='): 0x36,
    (INT, '&&'): 0x37,
    (INT, '||'): 0x38,
    (INT, '<<='): 0x39,
    (INT, '>>='): 0x3a,
    (INT, '&='): 0x3b,
    (INT, '|='): 0x3c,
    (INT, '^='): 0x3d,
    (STRING, '+'): 0x49,
}

def float2hex(f):
    return struct.unpack('<I', struct.pack('f', f))[0]

class Variable(object):
    def __init__(self, num, size):
        self.num = num
        self.size = size

class Function(object):
    def __init__(self, name, num, num_params=0, retval=False):
        self.name = name
        self.num = num
        self.locals = {}
        self.num_params = num_params
        self.retval = retval
        self.bc = [0x48]                    # Return

    def create_local(self, node):
        var = Variable(len(self.locals), node.size)
        self.locals[node] = var


class Compiler(object):
    def __init__(self, code):
        root = gen_ast(code)
        scope_pass(root)
        validate_pass(root)
        flatten_pass(root)

        self.root = root
        self.funcs = {
            DUMMY: Function(GLOBAL, 0),
            GLOBAL: Function(GLOBAL, 1),
        }
        self.strings = {MAGIC + code: 0}

        self.create_func_pass()
        for x in xrange(4):
            self.funcs[GLOBAL].locals[x] = Variable(x, 1)
        self.create_locals_pass()
        self.compile_func_pass()

    def create_string(self, s):
        if s not in self.strings:
            self.strings[s] = len(self.strings)
        assert len(self.strings) < 1024, 'Cannot create more than 1024 unique strings.'
        return self.strings[s]

    def create_locals_pass(self):
        def visitor(node, depth):
            if node is None:
                return node
            if isinstance(node, DeclNode) or isinstance(node, AssignNode) and node.decltype is not None:
                func = node.func
                if func is None:
                    func = self.funcs[GLOBAL]
                else:
                    func = self.funcs[func]
                func.create_local(node)
            return node
        Node.traverse(self.root, visitor, None)

    def create_func_pass(self):
        def visitor(node, depth):
            if node is None:
                return node
            if isinstance(node, FuncNode):
                self.create_func(node)
            return node
        Node.traverse(self.root, visitor, None)

    def create_func(self, node):
        func = Function(node.name, len(self.funcs), len(node.params), node.rettype is not VOID)
        self.funcs[node] = func

    def compile_func_pass(self):
        def visitor(node, depth):
            if node is None:
                return node
            if isinstance(node, FuncNode):
                self.compile_func(node)
            return node
        Node.traverse(self.root, visitor, None)

    def compile_func(self, node):
        self.fixups = []
        self.labels = {}
        self.bc = []
        self.func = node

        Node.traverse(node.body, self.pre_visitor, self.post_visitor)
        if len(self.bc) == 0 or self.bc[-1] != 0x48:
            self.bc += [0x48]

        for offset, label in self.fixups:
            self.bc[offset] = self.labels[label]
        self.funcs[node].bc = self.bc

        #print self.bc


    def pre_visitor(self, node, depth):
        if node is None:
            return node
        if isinstance(node, SubscriptNode):
            decl = node.decl
            if decl.is_global():
                num = self.funcs[GLOBAL].locals[decl].num
            else:
                num = self.funcs[self.func].locals[decl].num
            self.bc += [2]
            self.bc += [int(decl.is_global()), num]
        elif isinstance(node, LabelNode):
            self.labels[node.label] = len(self.bc)
        return node

    def post_visitor(self, node, depth):
        if node is None:
            return node
        if isinstance(node, LiteralNode):
            if node.vartype is INT:
                self.bc += [4, node.value]
            elif node.vartype is FLOAT:
                self.bc += [5, float2hex(node.value)]
            elif node.vartype is STRING:
                self.bc += [6, self.create_string(node.value)]
        elif isinstance(node, VarNode):
            decl = node.decl
            if isinstance(decl, FuncNode):
                num = self.funcs[decl].num
                # push an int literal
                self.bc += [4, num]
            else:
                if decl.is_global():
                    num = self.funcs[GLOBAL].locals[decl].num
                else:
                    num = self.funcs[self.func].locals[decl].num
                if node.lval:
                    self.bc += [2]
                elif node.vartype is INT or node.vartype is OBJECT:
                    self.bc += [0]
                elif node.vartype is FLOAT:
                    self.bc += [1]
                elif node.vartype is STRING:
                    self.bc += [3]
                self.bc += [int(decl.is_global()), num]
        elif isinstance(node, SubscriptNode):
            if node.lval:
                self.bc += [0x44]
            elif node.vartype is INT or node.vartype is OBJECT:
                self.bc += [0x42]
            elif node.vartype is FLOAT:
                self.bc += [0x43]
            elif node.vartype is STRING:
                self.bc += [0x42]
        elif isinstance(node, GotoNode):
            if node.cond is None:
                self.bc += [0x13]
            else:
                self.bc += [0x15]
            self.fixups += [(len(self.bc), node.target)]
            self.bc += [0x13371337]
        elif isinstance(node, ReturnNode):
            self.bc += [0x48]
        elif isinstance(node, CallNode):
            decl = node.decl
            if isinstance(decl, FuncNode):
                num = self.funcs[decl].num
                self.bc += [0x46, num]
            else:
                num = decl.num
                self.bc += [0x45, num]
        elif isinstance(node, UnOpNode):
            if (node.vartype, node.op) not in UOPS_MAP:
                raise Exception('Operation %s not compatible with %s' % (node.op, node.vartype))
            self.bc += [UOPS_MAP[(node.vartype, node.op)]]
        elif isinstance(node, BinOpNode):
            if (node.vartype, node.op) not in OPS_MAP:
                raise Exception('Operation %s not compatible with %s' % (node.op, node.vartype))
            self.bc += [OPS_MAP[(node.vartype, node.op)]]
        else:
            # print node
            pass

        return node

    def compile(self, fp):
        fp.write('SCRIPT03')
        fp.write('STRG')
        fp.write(struct.pack('<I', len(self.strings)))
        for s, i in sorted(self.strings.items(), key=lambda x: x[1]):
            fp.write(struct.pack('<I', len(s)) + s)
        fp.write('CODE')
        fp.write(struct.pack('<I', len(self.funcs)))
        for func in sorted(self.funcs.values(), key=lambda x: x.num):
            fp.write('FUNC')
            fp.write(struct.pack('<I', len(func.name)))
            fp.write(func.name)
            fp.write(struct.pack('<I', int(func.retval)))
            fp.write(struct.pack('<I', func.num_params))
            fp.write('SYMB')
            fp.write(struct.pack('<II', len(func.locals), 0))
            for var in sorted(func.locals.values(), key=lambda x: x.num):
                fp.write(struct.pack('<I', var.size))
            fp.write('DATA')
            bc = ''.join([struct.pack('<I', (x&0xFFFFFFFF)) for x in func.bc])
            fp.write(struct.pack('<I', len(bc)))
            fp.write(bc)
        size = fp.tell()
        fp.close()
        return {'size': size, 'strings': sorted(self.strings.items(), key=lambda x: x[1]), 'funcs': sorted(self.funcs.values(), key=lambda x: x.num)}


    def print_ast(self):
        print_ast(self.root)



code ='''
int x[10];
object test2()
{
    return Wall(x[2], x[1]);
}

void test(int a, object wall)
{
    WallOpen(wall);
}

void MapInitialize()
{
    x[2] = 7;
    x[1] = x[2];
    object wall = test2();
    test(3, wall);
    return;
}
'''
