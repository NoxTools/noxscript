from .ast import *

class CFGNode(object):
    def __init__(self, node):
        self.parents = set()
        self.children = set()
        self.nodes = [node]

    def add_child(self, child):
        self.children.add(child)
        child.parents.add(self)

    def remove_child(self, child):
        self.children.remove(child)
        child.parents.remove(self)

class CFGBlockNode(CFGNode):
    def __init__(self, cfg_nodes):
        super(CFGBlockNode, self).__init__(None)
        self.nodes = cfg_nodes[0].nodes + cfg_nodes[1].nodes
        self.cfg_nodes = cfg_nodes

class CFGIfNode(CFGNode):
    def __init__(self, cond, ifthen, ifelse):
        label = cond.nodes[0]
        super(CFGIfNode, self).__init__(label if isinstance(label, LabelNode) else None)
        self.cond = cond
        self.ifthen = ifthen
        self.ifelse = ifelse

class CFGWhileNode(CFGNode):
    def __init__(self, cond, body):
        label = cond.nodes[0]
        super(CFGWhileNode, self).__init__(label if isinstance(label, LabelNode) else None)
        self.cond = cond
        self.body = body
        self.continues = set()
        self.breaks = set()

def dce_pass(root):
    if len(root.parents) > 0:
        return
    children = list(root.children)
    for child in children:
        root.remove_child(child)
    for child in children:
        dce_pass(child)

def gen_cfg(ast_nodes):
    subgraphs = []
    label_map = {}
    cur = None
    for node in ast_nodes:
        if cur is None:
            cur = CFGNode(node)
            subgraphs.append(cur)
        else:
            child = CFGNode(node)
            cur.add_child(child)
            cur = child
        if isinstance(node, ReturnNode) or \
           (isinstance(node, GotoNode) and node.cond is None):
            cur = None
        if isinstance(node, LabelNode):
            label_map[node.label] = cur
    for graph in subgraphs:
        cur = graph
        while True:
            next_node = list(cur.children)[0] if len(cur.children) > 0 else None
            if isinstance(cur.nodes[0], GotoNode):
                cur.add_child(label_map[cur.nodes[0].target])
                if cur.nodes[0].cond is None:
                    cur.nodes.pop()
            if next_node is None:
                break
            cur = next_node
    for graph in subgraphs[1:]:
        dce_pass(graph)
    return subgraphs[0]

def coalesce_cfg(root):
    fake_root = CFGNode(None)
    fake_root.add_child(root)
    to_visit = [root]
    visited = set()
    while len(to_visit) > 0:
        cur = to_visit.pop(0)
        if cur in visited:
            continue
        if len(cur.children) > 0:
            to_visit += list(cur.children)
        if len(cur.children) == 1 and len(list(cur.children)[0].parents) == 1:
            child = list(cur.children)[0]
            cur.remove_child(child)
            for parent in set(cur.parents):
                parent.remove_child(cur)
                parent.add_child(child)
            child.nodes = cur.nodes + child.nodes
        visited.add(cur)
    root = list(fake_root.children)[0]
    fake_root.remove_child(root)
    return root

def print_cfg_dot(root):
    s = 'digraph CFG {\n'
    to_visit = [root]
    visited = set()
    while len(to_visit) > 0:
        cur = to_visit.pop(0)
        if cur in visited:
            continue
        if len(cur.children) > 0:
            to_visit += list(cur.children)
        s += '%d;\n' % id(cur)
        if len(cur.nodes):
            print id(cur), type(cur), cur.nodes[0], cur.nodes[-1]
        else:
            print id(cur), type(cur)
        for child in cur.children:
            s += '%d -> %d;\n' % (id(cur), id(child))
        visited.add(cur)
    s += '}'
    open('out.dot', 'wb').write(s)
    # print s

def ast_from_cfg(root, breaks=None, continues=None):
    if root is None:
        return None
    node = None
    if isinstance(root, CFGIfNode):
        node = BlockNode([])
        cond = ast_from_cfg(root.cond)
        node.children.append(cond)
        c = cond.children[-1]
        while not isinstance(c, GotoNode):
            assert isinstance(c, BlockNode)
            cond = c
            c = cond.children[-1]
        cond = cond.children.pop()
        ifnode = IfNode(cond.cond, ast_from_cfg(root.ifthen), ast_from_cfg(root.ifelse))
        node.children.append(ifnode)
    elif isinstance(root, CFGWhileNode):
        node = BlockNode([])
        cond = ast_from_cfg(root.cond)
        node.children.append(cond)
        cond = cond.children.pop()
        whilenode = WhileNode(cond.cond, ast_from_cfg(root.body, root.breaks, root.continues))
        node.children.append(whilenode)
    elif isinstance(root, CFGBlockNode):
        node = BlockNode([ast_from_cfg(node) for node in root.cfg_nodes])
    else:
        node = BlockNode(root.nodes)
    assert len(root.children) == 0
    return node
