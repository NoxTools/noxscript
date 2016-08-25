from .ast import *

import io
import json

def decl_to_string(node):
    if node.size > 1:
        return u'%s %s[%d]' % (node.decltype, node.name, node.size)
    else:
        return u'%s %s' % (node.decltype, node.name)

def value_to_string(value):
    if isinstance(value, str):
        return unicode(json.dumps(value, ensure_ascii=False))
    else:
        return unicode(repr(value))

def is_expression(node):
    return any(map(lambda t: isinstance(node, t), [LiteralNode, VarNode, BinOpNode, UnOpNode, CallNode, SubscriptNode]))

def is_statement(node):
    parent = node.parent
    return (isinstance(parent, FuncNode) and node == parent.body) \
        or isinstance(parent, BlockNode) \
        or (isinstance(parent, ForNode) and node == parent.body) \
        or (isinstance(parent, WhileNode) and node == parent.body) \
        or (isinstance(parent, IfNode) and node != parent.cond) \
        or isinstance(parent, GlobalNode)

def pre_visitor(stream, node, depth, visit):
    if node is None:
        return True

    if isinstance(node, FuncNode):
        stream.write(u'%s %s(%s)\n' % (node.rettype, node.name, u''.join([decl_to_string(x) for x in node.params])))
        visit(node.body)
        return False
    elif isinstance(node, DeclNode):
        # Global and local variables, excluding parameters
        stream.write(decl_to_string(node) + u';\n')
    elif isinstance(node, BlockNode):
        stream.write(u'{\n')
    elif isinstance(node, ForNode):
        stream.write(u'for (')
        visit(node.init)
        stream.write(u'; ')
        visit(node.cond)
        stream.write(u'; ')
        visit(node.inc)
        stream.write(u')\n')
        visit(node.body)
        return False
    elif isinstance(node, WhileNode):
        stream.write(u'while (')
        visit(node.cond)
        stream.write(u')\n')
        visit(node.body)
        return False
    elif isinstance(node, IfNode):
        stream.write(u'if (')
        visit(node.cond)
        stream.write(u')\n')
        visit(node.ifthen)
        if node.ifelse:
            if isinstance(node.ifelse, IfNode):
                stream.write(u'else ')
            else:
                stream.write(u'else\n')
            visit(node.ifelse)
        return False
    elif isinstance(node, BreakNode):
        stream.write(u'break;\n')
    elif isinstance(node, ContinueNode):
        stream.write(u'continue;\n')
    elif isinstance(node, ReturnNode):
        if node.value:
            stream.write(u'return ')
            visit(node.value)
            stream.write(u';\n')
        else:
            stream.write(u'return;\n')
        return False
    elif isinstance(node, LabelNode):
        stream.write(u'%s:\n' % node.label)
    elif isinstance(node, GotoNode):
        if node.cond:
            stream.write(u'if (false == ')
            visit(node.cond)
            stream.write(u') ')
        stream.write(u'goto %s;\n' % node.target)
        return False
    elif isinstance(node, LiteralNode):
        stream.write(value_to_string(node.value))
    elif isinstance(node, VarNode):
        stream.write(unicode(node.name))
    elif isinstance(node, BinOpNode):
        if isinstance(node, AssignNode) and node.decltype:
            stream.write(decl_to_string(node) + u' = ')
            visit(node.rhs)
            return False
        stmt = is_statement(node)
        if not stmt and (isinstance(node.parent, BinOpNode) or isinstance(node.parent, UnOpNode)):
            stream.write(u'(')
        visit(node.lhs)
        stream.write(u' %s ' % node.op)
        visit(node.rhs)
        if not stmt and (isinstance(node.parent, BinOpNode) or isinstance(node.parent, UnOpNode)):
            stream.write(u')')
        return False
    elif isinstance(node, UnOpNode):
        stream.write(unicode(node.op))
    elif isinstance(node, CallNode):
        stream.write(u'%s(' % node.callee)
        first = True
        for x in node.args:
            if not first:
                stream.write(u', ')
            else:
                first = False
            visit(x)
        stream.write(u')')
        return False
    elif isinstance(node, SubscriptNode):
        stream.write(u'%s[' % node.name)
        visit(node.subscript)
        stream.write(u']')
        return False
    return True

def post_visitor(stream, node, depth, visit):
    if node is None:
        return True

    if isinstance(node, BlockNode):
        stream.write(u'}\n')
    elif is_expression(node) and is_statement(node):
        stream.write(u';\n')

# Slightly different than Node.traverse
def traverse(node, preop, postop, depth=0):
    traverse_children = True
    visit = lambda node: traverse(node, preop, postop, depth + 1)
    if preop:
        traverse_children = preop(node, depth, visit)
    if traverse_children:
        if node is not None:
            for i in xrange(len(node.children)):
                if node.children[i] is not None:
                    node.children[i].parent = node
                traverse(node.children[i], preop, postop, depth+1)
    if postop:
        postop(node, depth, visit)

def unparse(root, stream=None):
    if stream is None:
        stream = io.StringIO()

    traverse(root, lambda *args: pre_visitor(stream, *args), lambda *args: post_visitor(stream, *args))
    return stream
