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

def validate_pass(root, add_comment=False):
    def visitor(add_comment, node, depth):
        if node is None:
            return node
        if add_comment:
            try:
                node.validate()
            except Exception as e:
                node.comment = 'FIXME %s' % str(e)
        else:
            node.validate()
        return node
    Node.traverse(root, lambda *args: visitor(add_comment, *args), None)

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

def remove_label_pass(root):
    def find_goto_visitor(labels, node, depth):
        if node is None:
            return node
        if isinstance(node, GotoNode):
            labels.add(node.target)
        return node

    def remove_label_visitor(labels, node, depth):
        if node is None:
            return node
        if isinstance(node, LabelNode) and node.label not in labels:
            return None
        return node

    labels = set()
    Node.traverse(root, lambda *args: find_goto_visitor(labels, *args), None)
    return Node.traverse(root, lambda *args: remove_label_visitor(labels, *args), None)

def coalesce_blocks_pass(root):
    def visitor(dirty, node, depth):
        if node is None:
            return node
        if isinstance(node, BlockNode):
            new_children = []
            for child in node.children:
                if child is None:
                    dirty['dirty'] = True
                    continue
                if not isinstance(child, LabelNode) and len(new_children) > 0 and \
                   (isinstance(new_children[-1], ReturnNode) or (isinstance(new_children[-1], GotoNode) and new_children[-1].cond is None)):
                    continue
                if isinstance(child, BlockNode):
                    new_children += child.children
                    dirty['dirty'] = True
                else:
                    new_children.append(child)

            # avoid eliminating top-most BlockNode
            if len(new_children) == 0 and hasattr(node, 'parent'):
                dirty['dirty'] = True
                return None
            if len(new_children) == 1 and hasattr(node, 'parent'):
                dirty['dirty'] = True
                return new_children[0]
            node.children = new_children
        return node

    dirty = {'dirty': False}
    root = Node.traverse(root, None, lambda *args: visitor(dirty, *args))
    return root, dirty['dirty']

# remove empty blocknode from conditionals
def empty_conditional_pass(root):
    def visitor(dirty, node, depth):
        if node is None:
            return node
        if isinstance(node, IfNode) and node.ifthen is None:
            if node.ifelse is None:
                dirty['dirty'] = True
                return None
            node.ifthen = node.ifelse
            node.ifelse = None
            node.cond = UnOpNode('!', node.cond)
            dirty['dirty'] = True
        return node

    dirty = {'dirty': False}
    root = Node.traverse(root, None, lambda *args: visitor(dirty, *args))
    return root, dirty['dirty']

# optimize condition expression
def reduce_conditional_pass(root):
    def visitor(dirty, node, depth):
        if node is None:
            return node
        if isinstance(node, IfNode) and node.ifthen is not None and node.ifelse is not None:
            if isinstance(node.ifthen, IfNode) and not isinstance(node.ifelse, IfNode):
                node.ifthen, node.ifelse = node.ifelse, node.ifthen
                node.cond = UnOpNode('!', node.cond)
                dirty['dirty'] = True
            elif (not isinstance(node.ifelse, IfNode) or isinstance(node.ifthen, IfNode)) \
              and isinstance(node.cond, BinOpNode) and node.cond.op == '!=':
                node.ifthen, node.ifelse = node.ifelse, node.ifthen
                node.cond = UnOpNode('!', node.cond)
                dirty['dirty'] = True
        return node

    dirty = {'dirty': False}
    root = Node.traverse(root, None, lambda *args: visitor(dirty, *args))
    return root, dirty['dirty']

def simplify_expr_pass(root):
    def visitor(dirty, node, depth):
        if node is None:
            return node
        if isinstance(node, UnOpNode) and isinstance(node.rhs, UnOpNode):
            if node.op == node.rhs.op:
                dirty['dirty'] = True
                return node.rhs.rhs
        if isinstance(node, UnOpNode) and isinstance(node.rhs, BinOpNode):
            if node.op == '!':
                if node.rhs.op == '==':
                    dirty['dirty'] = True
                    return BinOpNode('!=', node.rhs.lhs, node.rhs.rhs)
                if node.rhs.op == '!=':
                    dirty['dirty'] = True
                    return BinOpNode('==', node.rhs.lhs, node.rhs.rhs)

        return node

    dirty = {'dirty': False}
    root = Node.traverse(root, None, lambda *args: visitor(dirty, *args))
    return root, dirty['dirty']

def fix_unreferenced_pass(root):
    def visitor(used, node, dpeth):
        if node is None:
            return node

        if isinstance(node, VarNode) or isinstance(node, SubscriptNode):
            used.add(node.decl)
        return node

    def remove_visitor(used, node, dpeth):
        if node is None:
            return node

        if isinstance(node, DeclNode) and node not in used and not isinstance(node.parent, FuncNode):
            return None
        return node

    used = set()
    root = Node.traverse(root, None, lambda *args: visitor(used, *args))
    root = Node.traverse(root, None, lambda *args: remove_visitor(used, *args))
    return root

def decl_initializer_pass(root):
    # iterate over nodes and find the first use of a var, and check that
    # all other uses have it as a parent scope
    def visitor(uses, node, depth):
        if node is None:
            return node

        if isinstance(node, VarNode) or isinstance(node, SubscriptNode):
            decl = node.decl
            if decl.func != node.func or isinstance(decl.parent, FuncNode) or isinstance(decl, FuncNode):
                return node
            if decl in uses:
                first_use, first_scope, valid, others = uses[decl]
                if not any((x.lval for x in others)):
                    others.append(node)
                scope = node.scope
                while scope is not None and scope is not first_scope:
                    scope = scope.parent
                if scope is None:
                    uses[decl] = first_use, first_scope, False, others
            else:
                uses[decl] = (node.parent, node.scope, node.lval, [])
                uses[node.parent] = (decl,)
        return node

    def combine_visitor(uses, node, depth):
        if node is None:
            return node
        if node in uses:
            if isinstance(node, DeclNode):
                node.scope.remove(node.name, node)
                return None
            else:
                assign = AssignNode(node.op, node.lhs, node.rhs, uses[node][0].decltype)
                uses[assign] = uses[uses[node][0]]
                node.scope.add(assign.name, assign)
                assign.parent = node.parent
                return assign
        elif isinstance(node, VarNode) and not node.lval:
            decl = node.decl
            if decl in uses:
                first_use, first_scope, valid, others = uses[decl]
                # XXX while loops, for loops, gotos
                if first_scope != node.scope:
                    return node
                if node in others and valid and decl.rhs.is_constant():
                    return decl.rhs.copy()
        return node

    uses = {}
    root = Node.traverse(root, None, lambda *args: visitor(uses, *args))
    for k,v in uses.items():
        if len(v) == 4:
            first_use, first_scope, valid, others = v
            if not valid or not isinstance(first_use, BinOpNode) or first_use.op != '=' or k.size > 1:
                del uses[k]
                del uses[v[0]]
    root = Node.traverse(root, lambda *args: combine_visitor(uses, *args), None)
    return root
