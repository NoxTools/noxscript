from pyparsing import col, lineno

VOID = intern('void')
INT = intern('int')
FLOAT = intern('float')
STRING = intern('string')
OBJECT = intern('object')
FUNCTION = intern('function')
ANY = intern('any')
GLOBAL = intern('GLOBAL')

class AstException(Exception):
    def __init__(self, node, msg):
        if node.loc:
            Exception.__init__(self, '%s (line %d, col %d)' % (msg, node.lineno, node.col))
        else:
            Exception.__init__(self, '%s' % msg)

class Node(object):
    def __init__(self, loc=None):
        self.children = []
        self.loc = loc
        self._scope = None

    def __repr__(self):
        return '<%s>' % type(self).__name__

    @property
    def lineno(self):
        return None if self.loc is None else self.loc[0]

    @property
    def col(self):
        return None if self.loc is None else self.loc[1]

    @property
    def scope(self):
        if self._scope is None:
            return self.parent.scope
        return self._scope

    @property
    def func(self):
        return self.parent.func

    @property
    def vartype(self):
        return VOID

    @staticmethod
    def traverse(node, preop, postop, depth=0):
        if preop:
            node = preop(node, depth)
        if node is not None:
            for i in xrange(len(node.children)):
                if node.children[i] is not None:
                    node.children[i].parent = node
                node.children[i] = Node.traverse(node.children[i], preop, postop, depth+1)
        if postop:
            node = postop(node, depth)
        return node

    def scope_visitor(self):
        self._scope = None

    def validate(self):
        pass

    def find_ancestor(self, cls):
        if isinstance(self, cls):
            return self
        if self.parent is None:
            return None
        return self.parent.find_ancestor(cls)

    def is_constant(self):
        constant = all([node.is_constant() for node in self.children])
        return constant and len(self.children) > 0

class LiteralNode(Node):
    def __init__(self, value, **kwargs):
        super(LiteralNode, self).__init__(**kwargs)
        self.value = value

    def __repr__(self):
        return str(self.value)

    @property
    def vartype(self):
        if isinstance(self.value, str):
            return STRING
        elif isinstance(self.value, float):
            return FLOAT
        else:
            return INT

    @classmethod
    def from_tokens(cls, st, loc, toks):
        return cls(toks[0], loc=(lineno(loc, st), col(loc, st)))

    def is_constant(self):
        return True

class VarNode(Node):
    def __init__(self, name, **kwargs):
        super(VarNode, self).__init__(**kwargs)
        self.name = name
        self.lval = False

    def __repr__(self):
        return '<VarNode %s>' % self.name

    @property
    def decl(self):
        return self.scope.get(self.name)

    @property
    def vartype(self):
        node = self.decl
        if node is None:
            raise AstException(self, '%s not defined' % self.name)
        elif isinstance(node, DeclNode) and node.size > 1:
            raise AstException(self, 'Array must be subscripted')
        return node.decltype

    @classmethod
    def from_tokens(cls, st, loc, toks):
        toks = toks[0]
        return cls(toks[0], loc=(lineno(loc, st), col(loc, st)))

class BinOpNode(Node):
    def __init__(self, op, lhs, rhs, **kwargs):
        super(BinOpNode, self).__init__(**kwargs)
        self.op = op
        self.children = [lhs, rhs]

    def __repr__(self):
        return '<BinOp %s>' % self.op

    @property
    def lhs(self):
        return self.children[0]
    @property
    def rhs(self):
        return self.children[1]

    @property
    def vartype(self):
        if self.lhs.vartype is not self.rhs.vartype and self.lhs.vartype is not ANY and self.rhs.vartype is not ANY:
            # print self.lhs, self.rhs
            raise AstException(self, '\'%s\' with wrong type (%s is not %s)' % (self.op, self.lhs.vartype, self.rhs.vartype))
        if self.op in '< > <= >= != =='.split(' '):
            # comparisons always produce an integer
            return INT
        if self.lhs.vartype is ANY:
            return self.rhs.vartype
        else:
            return self.lhs.vartype

    @classmethod
    def from_tokens(cls, st, loc, toks):
        assert len(toks) == 1
        toks = toks[0]
        node = toks[0]
        for x in xrange(1, len(toks), 2):
            node = cls(toks[x], node, toks[x+1], loc=(lineno(loc, st), col(loc, st)))
        return node

    def validate(self):
        if self.op in '= += -= *= /= %='.split(' '):
            if isinstance(self.lhs, VarNode) or isinstance(self.lhs, SubscriptNode):
                self.lhs.lval = True
            else:
                raise AstException(self, 'Invalid lvalue')

class AssignNode(BinOpNode):
    def __init__(self, op, lhs, rhs, decltype=None, **kwargs):
        super(AssignNode, self).__init__(op, lhs, rhs, **kwargs)
        self.decltype = intern(decltype) if decltype else None

    def __repr__(self):
        return '<AssignNode %s %s>' % (self.op, self.decltype)

    @property
    def size(self):
        return 1

    @property
    def name(self):
        return self.lhs.name

    @classmethod
    def from_tokens(cls, st, loc, toks):
        return cls('=', VarNode(toks[1]), toks[2], toks[0], loc=(lineno(loc, st), col(loc, st)))

    @classmethod
    def from_tokens_op(cls, st, loc, toks):
        assert len(toks) == 1
        toks = toks[0]
        assert len(toks) == 3
        return cls(toks[1], toks[0], toks[2], loc=(lineno(loc, st), col(loc, st)))

    def is_global(self):
        return self.func is None or self.func.name is GLOBAL

    def scope_visitor(self):
        if self.decltype is not None:
            self.scope.add(self.lhs.name, self)

    def validate(self):
        super(AssignNode, self).validate()

        if self.func == None:
            if not self.decltype:
                raise AstException(self, '%s missing declaration type' % self.name)
            if not self.rhs.is_constant():
                raise AstException(self, '%s initializer must be a constant expression' % self.name)

class UnOpNode(Node):
    def __init__(self, op, rhs, **kwargs):
        super(UnOpNode, self).__init__(**kwargs)
        self.op = op
        self.children = [rhs]

    def __repr__(self):
        return '<UnOpNode %s>' % self.op

    @property
    def rhs(self):
        return self.children[0]

    @property
    def vartype(self):
        return self.rhs.vartype

    @classmethod
    def from_tokens(cls, st, loc, toks):
        assert len(toks) == 1
        toks = toks[0]
        assert len(toks) == 2
        return cls(toks[0], toks[1], loc=(lineno(loc, st), col(loc, st)))

class CallNode(Node):
    def __init__(self, callee, args, **kwargs):
        super(CallNode, self).__init__(**kwargs)
        self.callee = callee
        self.children = args

    def __repr__(self):
        return '<CallNode %s>' % self.callee

    @property
    def args(self):
        return self.children

    @property
    def decl(self):
        return self.scope.get(self.callee)

    @property
    def vartype(self):
        node = self.decl
        return node.rettype

    def scope_visitor(self):
        # Once we have a scope, fix order of arguments
        if not isinstance(self.decl, BuiltinNode):
            self.children.reverse()

    def validate(self):
        node = self.decl
        if node is None:
            raise AstException(self, '%s is not defined' % self.callee)
        if not isinstance(node, FuncNode) and not isinstance(node, BuiltinNode):
            raise AstException(self, '%s is not a function' % self.callee)
        params = [x.decltype for x in node.params]
        if len(params) != len(self.children):
            raise AstException(self, 'Invalid arguments for \'%s\': expected %d, got %d' % (node.name, len(params), len(self.children)))
        if not isinstance(node, BuiltinNode):
            params.reverse()
        for i in xrange(len(params)):
            if params[i] is not ANY and self.children[i].vartype is not ANY and params[i] is not self.children[i].vartype:
                raise AstException(self, 'Wrong type for \'%s\': expected %s, got %s' % (node.name, params[i], self.children[i].vartype))

    @classmethod
    def from_tokens(cls, st, loc, toks):
        return cls(toks[0], toks[1:], loc=(lineno(loc, st), col(loc, st)))

class ReturnNode(Node):
    def __init__(self, value=None, **kwargs):
        super(ReturnNode, self).__init__(**kwargs)
        self.children = [value]

    @property
    def value(self):
        return self.children[0]

    def validate(self):
        vartype = self.value.vartype if self.value is not None else VOID
        node = self.func
        if node.rettype is not vartype:
            raise AstException(self, 'Function return type mismatch: expected %s, got %s' % (node.rettype, self.value.vartype))

    @classmethod
    def from_tokens(cls, st, loc, toks):
        return cls(*toks, loc=(lineno(loc, st), col(loc, st)))

class BreakNode(Node):
    @classmethod
    def from_tokens(cls, st, loc, toks):
        return cls(loc=(lineno(loc, st), col(loc, st)))

class ContinueNode(Node):
    @classmethod
    def from_tokens(cls, st, loc, toks):
        return cls(loc=(lineno(loc, st), col(loc, st)))

class GotoNode(Node):
    def __init__(self, target, cond=None, **kwargs):
        super(GotoNode, self).__init__(**kwargs)
        self.target = target
        self.children = [cond]

    def __repr__(self):
        return '<GotoNode %s>' % self.target

    @property
    def cond(self):
        return self.children[0]

    @classmethod
    def from_tokens(cls, st, loc, toks):
        return cls(toks[0], loc=(lineno(loc, st), col(loc, st)))

class LabelNode(Node):
    def __init__(self, label, **kwargs):
        super(LabelNode, self).__init__(**kwargs)
        self.label = label

    def __repr__(self):
        return '<LabelNode %s>' % self.label

    @classmethod
    def from_tokens(cls, st, loc, toks):
        return cls(toks[0], loc=(lineno(loc, st), col(loc, st)))

    def scope_visitor(self):
        self.func.scope.add(self.label, self)

class DeclNode(Node):
    def __init__(self, decltype, name, size=None, **kwargs):
        super(DeclNode, self).__init__(**kwargs)
        self.decltype = intern(decltype)
        self.name = name
        if size is not None and size <= 1:
            raise AstException(self, 'Array size must be greater than 1')
        self.size = size or 1

    def __repr__(self):
        return '<DeclNode %s %s %d>' % (self.decltype, self.name, self.size)

    def is_global(self):
        return self.func is None or self.func.name is GLOBAL

    @classmethod
    def from_tokens(cls, st, loc, toks):
        return cls(*toks, loc=(lineno(loc, st), col(loc, st)))

    def scope_visitor(self):
        self.scope.add(self.name, self)

class SubscriptNode(Node):
    def __init__(self, name, sub, **kwargs):
        super(SubscriptNode, self).__init__(**kwargs)
        self.name = name
        self.children = [sub]
        self.lval = False

    def __repr__(self):
        return '<SubscriptNode %s>' % self.name

    @property
    def subscript(self):
        return self.children[0]

    @property
    def decl(self):
        return self.scope.get(self.name)

    @property
    def vartype(self):
        node = self.decl
        if node is None:
            raise AstException(self, '%s is not defined' % self.name)
        elif node.size <= 1:
            raise AstException(self, '%s is not an array' % self.name)
        return node.decltype

    @classmethod
    def from_tokens(cls, st, loc, toks):
        return cls(*toks, loc=(lineno(loc, st), col(loc, st)))

class IfNode(Node):
    def __init__(self, cond, ifthen, ifelse=None, **kwargs):
        super(IfNode, self).__init__(**kwargs)
        self.children = [cond, ifthen, ifelse]

    @property
    def cond(self):
        return self.children[0]

    @property
    def ifthen(self):
        return self.children[1]

    @property
    def ifelse(self):
        return self.children[2]

    @classmethod
    def from_tokens(cls, st, loc, toks):
        return cls(*toks, loc=(lineno(loc, st), col(loc, st)))

    def validate(self):
        if self.cond.vartype is not INT:
            raise AstException(self, 'Condition must be int-type')

class WhileNode(Node):
    def __init__(self, cond, body, **kwargs):
        super(WhileNode, self).__init__(**kwargs)
        self.children = [cond, body]

    @property
    def cond(self):
        return self.children[0]
    
    @property
    def body(self):
        return self.children[1]

    @classmethod
    def from_tokens(cls, st, loc, toks):
        return cls(*toks, loc=(lineno(loc, st), col(loc, st)))

    def validate(self):
        if self.cond.vartype is not INT:
            raise AstException(self, 'Condition must be int-type')

class ForNode(Node):
    def __init__(self, init, cond, inc, body, **kwargs):
        super(ForNode, self).__init__(**kwargs)
        self.children = [init, cond, inc, body]

    @property
    def init(self):
        return self.children[0]

    @property
    def cond(self):
        return self.children[1]

    @property
    def inc(self):
        return self.children[2]

    @property
    def body(self):
        return self.children[3]

    @classmethod
    def from_tokens(cls, st, loc, toks):
        return cls(*toks, loc=(lineno(loc, st), col(loc, st)))

    def scope_visitor(self):
        self._scope = Scope(self.parent.scope)

    def validate(self):
        if self.cond is not None:
            if self.cond.vartype is not INT:
                raise AstException(self, 'Condition must be int-type')

class BlockNode(Node):
    def __init__(self, nodes, **kwargs):
        super(BlockNode, self).__init__(**kwargs)
        self.children = nodes

    @classmethod
    def from_tokens(cls, st, loc, toks):
        return cls(*toks, loc=(lineno(loc, st), col(loc, st)))

    def scope_visitor(self):
        self._scope = Scope(self.parent.scope)

class BuiltinNode(Node):
    def __init__(self, num, rettype, name, params):
        self.num = num
        self.rettype = intern(rettype)
        self.name = name
        self.params = [DeclNode(param, None) for param in params]

class FuncNode(Node):
    def __init__(self, rettype, name, params, body, **kwargs):
        super(FuncNode, self).__init__(**kwargs)
        self.rettype = intern(rettype)
        self.name = name
        self.tmp_id = 0
        self.children = params + [body]
        self.decltype = FUNCTION

    def __repr__(self):
        return '<FuncNode %s %s>' % (self.rettype, self.name)

    @property
    def func(self):
        return self

    @property
    def params(self):
        return self.children[:-1]

    @property
    def body(self):
        return self.children[-1]

    @body.setter
    def body(self, value):
        self.children[-1] = value

    @classmethod
    def from_tokens(cls, st, loc, toks):
        return cls(toks[0], toks[1], toks[2:-1], toks[-1], loc=(lineno(loc, st), col(loc, st)))

    def new_label(self):
        node = LabelNode('.L%d' % self.tmp_id)
        self.tmp_id += 1
        self.scope.add(node.label, node)
        return node

    def scope_visitor(self):
        self._scope = Scope(self.parent.scope)
        self.parent.scope.add(self.name, self)

class GlobalNode(Node):
    def __init__(self, children):
        super(GlobalNode, self).__init__()
        self.children = children if isinstance(children, list) else children.asList()
        self.parent = None

    @property
    def func(self):
        return None

    @classmethod
    def from_tokens(cls, st, loc, toks):
        return cls(toks)

    def scope_visitor(self):
        self._scope = Scope(None)

class Scope(object):
    def __init__(self, parent):
        self.parent = parent
        self.names = {}

    def get(self, name):
        node = self.names.get(name, None)
        if node is None and self.parent is not None:
            node = self.parent.get(name)
        return node

    def add(self, name, node):
        if self.get(name) is not None:
            raise AstException(node, '%s is already defined' % name)
        self.names[name] = node

def print_ast(root):
    def visitor(node, depth):
        if node is None:
            return node
        print '%s%s (%s)' % (' '*depth*2, node, node.vartype)
        return node
    Node.traverse(root, visitor, None)

