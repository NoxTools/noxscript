from .ast import *
from .builtins import BUILTINS
from .cfg import *
from .passes import *
from .struct_analysis import *
from .unparser import unparse

import io
import struct

BUILTINS_MAP = {}
for name, bi in BUILTINS.items():
    BUILTINS_MAP[bi['num']] = (bi['name'], intern(bi['rettype']), len(bi['args']))

VAR_MAP = {
    0x00: INT,
    0x01: FLOAT,
    0x02: ANY,
    0x03: STRING,
}
ARRAY_MAP = {
    0x42: ANY,
    0x43: FLOAT,
    0x44: ANY,
}
LITERAL_MAP = {
    0x04: INT,
    0x05: FLOAT,
    0x06: STRING,
}
UOPS_MAP = {
    0x3e: (INT, '!'),
    0x3f: (INT, '~'),
    0x40: (INT, '-'),
    0x41: (FLOAT, '-'),
}
OPS_MAP = {
    0x07: (INT, '+'),
    0x08: (FLOAT, '+'),
    0x09: (INT, '-'),
    0x0a: (FLOAT, '-'),
    0x0b: (INT, '*'),
    0x0c: (FLOAT, '*'),
    0x0d: (INT, '/'),
    0x0e: (FLOAT, '/'),
    0x0f: (INT, '%'),
    0x10: (INT, '&'),
    0x11: (INT, '|'),
    0x12: (INT, '^'),
    0x16: (INT, '='),
    0x17: (FLOAT, '='),
    0x18: (STRING, '='),
    0x19: (INT, '*='),
    0x1a: (FLOAT, '*='),
    0x1b: (INT, '/='),
    0x1c: (FLOAT, '/='),
    0x1d: (INT, '+='),
    0x1e: (FLOAT, '+='),
    0x1f: (STRING, '+='),
    0x20: (INT, '-='),
    0x21: (FLOAT, '-='),
    0x22: (INT, '%='),
    0x23: (INT, '=='),
    0x24: (FLOAT, '=='),
    0x25: (STRING, '=='),
    0x26: (INT, '<<'),
    0x27: (INT, '>>'),
    0x28: (INT, '<'),
    0x29: (FLOAT, '<'),
    0x2a: (STRING, '<'),
    0x2b: (INT, '>'),
    0x2c: (FLOAT, '>'),
    0x2d: (STRING, '>'),
    0x2e: (INT, '<='),
    0x2f: (FLOAT, '<='),
    0x30: (STRING, '<='),
    0x31: (INT, '>='),
    0x32: (FLOAT, '>='),
    0x33: (STRING, '>='),
    0x34: (INT, '!='),
    0x35: (FLOAT, '!='),
    0x36: (STRING, '!='),
    0x37: (INT, '&&'),
    0x38: (INT, '||'),
    0x39: (INT, '<<='),
    0x3a: (INT, '>>='),
    0x3b: (INT, '&='),
    0x3c: (INT, '|='),
    0x3d: (INT, '^='),
    0x49: (STRING, '+'),
}

def hex2float(f):
    return struct.unpack('f', struct.pack('<I', f))[0]

class Variable(object):
    def __init__(self, name, num, size):
        self.name = name
        self.num = num
        self.size = size if size > 1 else None

        self.node = DeclNode(ANY, self.name, self.size)

    def __repr__(self):
        return 'Variable<%d>(%s, %d)' % (self.num, self.name, self.size or 1)

class Function(object):
    def __init__(self, name, num, num_params, retval):
        self.name = name
        self.num = num
        self.locals = []
        self.num_params = num_params
        self.retval = retval
        self.bc = []

    def __repr__(self):
        return 'Function<%d>(%s, %d, %s, %d)' % (self.num, self.name, self.num_params, str(self.retval), len(self.locals))

class Decompiler(object):
    def __init__(self, fp):
        self.load_file(fp)

        self.root = GlobalNode([])
        for f in self.funcs:
            if f.num == 0:
                continue
            params = [f.locals[i].node for i in xrange(f.num_params)]
            f.node = FuncNode(ANY if f.retval else VOID, f.name, params, None)
            if f.num == 1:
                self.global_func = f
            else:
                self.root.children.append(f.node)
        for f in self.funcs:
            if f.num == 0:
                continue
            body = self.parse_function(f)
            f.node.body = body

            if f == self.global_func:
                self.root.children += filter(lambda node: not isinstance(node, ReturnNode), body.children)

        scope_pass(self.root)
        while self.infer_types_pass(self.root):
            pass # print 'here'
        # print_ast(self.root)
        try:
            validate_pass(self.root)
        except Exception as e:
            print 'Error detected in AST: %s' % e
        # print_ast(self.funcs[10].node)
        unparse(self.root, io.TextIOWrapper(io.BufferedWriter(io.FileIO('dump.txt', 'w'))))

    def parse_function(self, f):
        block = BlockNode([])
        stack = []
        positions = {}
        position_stack = []
        labels = {}

        i = 0
        while i < len(f.bc):
            pos = i
            opcode = f.bc[i]
            i += 1
            if opcode in UOPS_MAP:
                t, op = UOPS_MAP[opcode]
                node = UnOpNode(op, stack.pop())
                pos = position_stack.pop()
                node.optype = t
            elif opcode in OPS_MAP:
                t, op = OPS_MAP[opcode]
                rhs = stack.pop()
                lhs = stack.pop()
                pos = position_stack.pop()
                pos = position_stack.pop()
                node = BinOpNode(op, lhs, rhs)
                node.optype = t
            elif opcode in VAR_MAP:
                t = VAR_MAP[opcode]
                is_global = bool(f.bc[i])
                i += 1
                num = f.bc[i]
                i += 1
                if is_global:
                    if num == 0:
                        node = LiteralNode(-2)
                        node.keyword = 'other'
                    elif num == 1:
                        node = LiteralNode(-1)
                        node.keyword = 'self'
                    elif num == 2:
                        node = LiteralNode(1)
                        node.keyword = 'true'
                    elif num == 3:
                        node = LiteralNode(0)
                        node.keyword = 'false'
                    else:
                        node = VarNode(self.global_func.locals[num].name)
                else:
                    node = VarNode(f.locals[num].name)
                node.optype = t
                if opcode == 0x02:
                    node.lval = True
            elif opcode in LITERAL_MAP:
                t = LITERAL_MAP[opcode]
                x = f.bc[i]
                i += 1
                if t is STRING:
                    x = self.strings[x]
                elif t is FLOAT:
                    x = hex2float(x)
                node = LiteralNode(x)
            elif opcode in [0x13, 0x14, 0x15]: # jnz
                idx = f.bc[i]
                i += 1
                if idx not in labels:
                    labels[idx] = 'L' + str(idx)
                if opcode == 0x13:
                    node = GotoNode(labels[idx])
                elif opcode == 0x14:
                    node = GotoNode(labels[idx], UnOpNode('!', stack.pop()))
                elif opcode == 0x15:
                    node = GotoNode(labels[idx], stack.pop())
                    pos = position_stack.pop()
            elif opcode in ARRAY_MAP:
                subscript = stack.pop()
                varnode = stack.pop()
                pos = position_stack.pop()
                pos = position_stack.pop()
                node = SubscriptNode(varnode.name, subscript)
                node.optype = ARRAY_MAP[opcode]
                if opcode == 0x44:
                    node.lval = True
            elif opcode == 0x45: # built-in
                num = f.bc[i]
                i += 1
                name, rettype, num_params = BUILTINS_MAP[num]
                args = [stack.pop() for _ in xrange(num_params)]
                for _ in xrange(num_params):
                    pos = position_stack.pop()
                args.reverse()
                node = CallNode(name, args)
            elif opcode == 0x46:
                num = f.bc[i]
                i += 1
                args = [stack.pop() for _ in xrange(self.funcs[num].num_params)]
                for _ in xrange(self.funcs[num].num_params):
                    pos = position_stack.pop()
                node = CallNode(self.funcs[num].name, args)
            elif opcode in [0x47, 0x48]:
                # NoxC compiler always adds a return void to the end
                # of a function. Ignore it if we have a retval.
                if i == len(f.bc) and opcode == 0x48 and f.retval:
                    continue
                if f.retval:
                    node = ReturnNode(stack.pop())
                    pos = position_stack.pop()
                else:
                    node = ReturnNode()
            else:
                raise Exception('Missing handler for opcode 0x%02X' % opcode)
            positions[node] = pos
            position_stack.append(pos)
            stack.append(node)
        for node, i in positions.items():
            if i not in labels:
                del positions[node]
        for node in stack:
            if node in positions:
                block.children.append(LabelNode(labels[positions[node]]))
            block.children.append(node)

        block, _ = coalesce_blocks_pass(block)
        cfg_root = coalesce_cfg(gen_cfg(block.children))
        cfg_root = analyze(cfg_root)
        ast_root = ast_from_cfg(cfg_root)
        ast_root = remove_label_pass(ast_root)
        while True:
            ast_root, dirty = coalesce_blocks_pass(ast_root)
            if dirty:
                continue
            ast_root, dirty = empty_conditional_pass(ast_root)
            if dirty:
                continue
            ast_root, dirty = simplify_expr_pass(ast_root)
            if dirty:
                continue
            ast_root, dirty = reduce_conditional_pass(ast_root)
            if dirty:
                continue
            break
        block = ast_root

        for i in xrange(f.num_params, len(f.locals)):
            if f == self.global_func and i < 4:
                continue
            block.children.insert(0, f.locals[i].node)
        return block

    def infer_types_pass(self, root):
        def pre_visitor(self, node, depth):
            if node is None:
                return node
            parent = node.parent
            if isinstance(node, VarNode) or isinstance(node, SubscriptNode):
                if hasattr(parent, 'optype'):
                    t = parent.optype
                    if isinstance(parent, BinOpNode) and parent.op in ['=', '==', '!=']:
                        other = parent.rhs if node == parent.lhs else parent.lhs
                        if t is INT and other.vartype is not ANY:
                            t = other.vartype
                elif isinstance(parent, CallNode):
                    decl = parent.decl
                    params = [x.decltype for x in decl.params]
                    for i in xrange(len(params)):
                        if parent.args[i] == node:
                            t = params[i]
                            break
                elif isinstance(parent, SubscriptNode):
                    t = INT
                else:
                    t = ANY

                decl = node.decl
                if t is not ANY and (decl.decltype is ANY or (decl.decltype is INT and t is not INT)):
                    decl.decltype = t
                    self.dirty = True
            elif isinstance(node, LiteralNode):
                if isinstance(parent, CallNode):
                    decl = parent.decl
                    params = [x.decltype for x in decl.params]
                    for i in xrange(len(params)):
                        if parent.args[i] == node:
                            if params[i] is FUNCTION and node.vartype is INT:
                                node = VarNode(self.funcs[node.value].name)
                                self.dirty = True
                            elif params[i] is not ANY and params[i] != node.vartype:
                                print node, node.vartype, params[i]
            elif isinstance(node, ReturnNode) and node.value:
                if node.value.vartype is not node.func.rettype:
                    node.func.rettype = node.value.vartype
                    self.dirty = True
            elif isinstance(node, CallNode):
                decl = node.decl
                params = [x.decltype for x in decl.params]
                for i in xrange(len(params)):
                    if params[i] is ANY and node.args[i].vartype is not ANY:
                        decl.params[i].decltype = node.args[i].vartype
                        self.dirty = True
            return node
        self.dirty = False
        Node.traverse(root, lambda n, d: pre_visitor(self, n, d), None)
        return self.dirty

    def load_file(self, fp):
        def read_uint(fp):
            return struct.unpack('<I', fp.read(4))[0]
        def read_string(fp):
            return fp.read(read_uint(fp))
        def read_token(fp, tok):
            assert fp.read(len(tok)) == tok
        read_token(fp, 'SCRIPT03')
        read_token(fp, 'STRG')
        num_strings = read_uint(fp)
        self.strings = map(lambda x: read_string(fp), xrange(num_strings))
        read_token(fp, 'CODE')
        num_funcs = read_uint(fp)
        self.funcs = []
        for num in xrange(num_funcs):
            read_token(fp, 'FUNC')
            name = read_string(fp)
            retval = bool(read_uint(fp))
            num_params = read_uint(fp)
            func = Function(name, num, num_params, retval)
            self.funcs.append(func)

            read_token(fp, 'SYMB')
            num_locals = read_uint(fp)
            fp.read(4) # ignored
            prefix = 'gvar' if num == 1 else 'var'
            func.locals = map(lambda x: Variable(('arg' if x < num_params else prefix) + str(x), x, read_uint(fp)), xrange(num_locals))

            read_token(fp, 'DATA')
            bc_length = read_uint(fp)
            assert bc_length % 4 == 0
            func.bc = map(lambda x: read_uint(fp), xrange(bc_length / 4))
