from .ast import *
from .builtins import BUILTINS

def scope_pass(root):
    def visitor(node, depth):
        if node is None:
            return node
        node.scope_visitor()
        if isinstance(node, GlobalNode):
            for bi in BUILTINS.values():
                node.scope.add(bi['name'], BuiltinNode(bi['num'], intern(bi['rettype']), bi['name'], [intern(x['type']) for x in bi['args']]))
        return node
    Node.traverse(root, visitor, None)

def validate_pass(root):
    def visitor(node, depth):
        if node is None:
            return node
        node.validate()
        return node
    Node.traverse(root, visitor, None)

def flatten_pass(root):
    def pre_visitor(node, depth):
        if node is None:
            return node
        if isinstance(node, WhileNode):
            func = node.func
            node.begin_label = func.new_label()
            node.end_label = func.new_label()
        if isinstance(node, ForNode):
            func = node.func
            node.begin_label = func.new_label()
            node.inc_label = func.new_label()
            node.end_label = func.new_label()
        return node

    def post_visitor(node, depth):
        if node is None:
            return node
        if isinstance(node, IfNode):
            func = node.func
            end_label = func.new_label()
            if node.ifelse:
                else_label = func.new_label()
                nodes = [
                    GotoNode(else_label.label, node.cond),
                    node.ifthen,
                    GotoNode(end_label.label),
                    else_label,
                    node.ifelse,
                    end_label
                ]
            else:
                nodes = [
                    GotoNode(end_label.label, node.cond),
                    node.ifthen,
                    end_label
                ]
            return BlockNode(nodes)
        if isinstance(node, WhileNode):
            func = node.func
            begin_label = node.begin_label
            end_label = node.end_label
            nodes = [
                begin_label,
                GotoNode(end_label.label, node.cond),
                node.body,
                GotoNode(begin_label.label),
                end_label
            ]
            return BlockNode(nodes)
        if isinstance(node, ForNode):
            func = node.func
            begin_label = node.begin_label
            inc_label = node.inc_label
            end_label = node.end_label
            nodes = []
            if node.init:
                nodes += [node.init]
            nodes += [
                begin_label,
                GotoNode(end_label.label, node.cond),
                node.body,
                inc_label
            ]
            if node.inc:
                nodes += [node.inc]
            nodes += [
                GotoNode(begin_label.label),
                end_label
            ]
            return BlockNode(nodes)
        if isinstance(node, ContinueNode):
            anc = node.find_ancestor([WhileNode, ForNode])
            if anc is None:
                raise Exception('Could not find loop')
            if isinstance(anc, ForNode):
                return GotoNode(anc.inc_label.label)
            return GotoNode(anc.begin_label.label)
        if isinstance(node, BreakNode):
            anc = node.find_ancestor([WhileNode, ForNode])
            if anc is None:
                raise Exception('Could not find loop')
            return GotoNode(anc.end_label.label)
        return node

    Node.traverse(root, pre_visitor, post_visitor)
