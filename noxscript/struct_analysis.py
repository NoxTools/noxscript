from .cfg import *

def find_cycle(root, visited=None, find=None):
    if visited is None:
        visited = []
    if find is None:
        find = root
    if root in visited:
        cycle = visited[visited.index(root):]
        if find in cycle:
            return cycle
        else:
            return None
    visited.append(root)
    for child in list(root.children):
        cycle = find_cycle(child, visited, find)
        if cycle is not None:
            return cycle
    visited.pop()
    return None

def dfs(root):
    to_visit = [root]
    visited = list()
    while len(to_visit) > 0:
        cur = to_visit.pop()
        if cur in visited:
            continue
        if len(cur.children) > 0:
            to_visit += list(cur.children)
        visited.append(cur)
    return visited

def analyze(root):
    counter = 0
    fake_root = CFGNode(None)
    fake_root.add_child(root)
    while counter < 150:
        nodes = dfs(list(fake_root.children)[0])
        if any((reduce_conditional(node) for node in nodes)):
            counter += 1
            continue
        if any((reduce_block(node) for node in nodes)):
            counter += 1
            continue
        if any((reduce_cyclic(node) for node in nodes)):
            counter += 1
            continue
        break
    root = list(fake_root.children)[0]
    fake_root.remove_child(root)
    return root

def reduce_block(entry):
    if len(entry.children) == 1:
        child = list(entry.children)[0]
        if len(child.parents) == 1:
            block_node = CFGBlockNode([entry, child])
            entry.remove_child(child)
            for node in list(entry.parents):
                node.remove_child(entry)
                node.add_child(block_node)
            for node in list(child.children):
                child.remove_child(node)
                block_node.add_child(node)
            return True
    return False

def reduce_conditional(entry):
    children = list(entry.children)
    if len(children) != 2:
        return False
    left, right = children
    if len(left.parents) == 1 and len(right.parents) == 1 and \
       len(left.children) <= 1 and len(right.children) <= 1 and \
       (len(left.children) == 0 or len(right.children) == 0 or \
        list(left.children)[0] is list(right.children)[0]):
        goto_node = entry.nodes[-1]
        ifelse = left if len(left.nodes) > 0 and isinstance(left.nodes[0], LabelNode) and left.nodes[0].label == goto_node.target else right
        ifthen = right if ifelse is left else left

        ifnode = CFGIfNode(entry, ifthen, ifelse)

        entry.remove_child(left)
        for child in list(left.children):
            left.remove_child(child)
            ifnode.add_child(child)
        entry.remove_child(right)
        for child in list(right.children):
            right.remove_child(child)
            ifnode.add_child(child)

        for parent in list(entry.parents):
            parent.remove_child(entry)
            parent.add_child(ifnode)
        return True

    for x in [(left, right), (right, left)]:
        left, right = x
        if len(left.parents) == 1 and (len(left.children) == 0 or \
        (len(left.children) == 1 and list(left.children)[0] is right)):
            assert right.nodes[0].label is entry.nodes[-1].target
            ifnode = CFGIfNode(entry, left, None)
            entry.remove_child(left)
            for child in list(left.children):
                left.remove_child(child)
                ifnode.add_child(child)
            entry.remove_child(right)
            ifnode.add_child(right)
            for parent in list(entry.parents):
                parent.remove_child(entry)
                parent.add_child(ifnode)
            return True
    return False

def reduce_cyclic(entry):
    cycle = find_cycle(entry)
    if cycle is None:
        return False
    for node in cycle:
        if any([x not in cycle for x in node.parents]):
            cond_node = node
            break
    cond_children = list(cond_node.children)
    if cond_children[0] in cycle:
        body_node, exit_node = cond_children
    else:
        exit_node, body_node = cond_children

    assert exit_node.nodes[0].label == cond_node.nodes[-1].target

    while_node = CFGWhileNode(cond_node, body_node)
    nodes = dfs(body_node)
    for node in nodes:
        if len(node.children) == 1:
            child = list(node.children)[0]
            if child is exit_node:
                node.remove_child(child)
                node.add_child(CFGNode(BreakNode()))
            elif child is cond_node:
                node.remove_child(child)
                node.add_child(CFGNode(ContinueNode()))
    cond_node.remove_child(exit_node)
    cond_node.remove_child(body_node)
    while_node.add_child(exit_node)
    for parent in list(cond_node.parents):
        parent.remove_child(cond_node)
        parent.add_child(while_node)
    while_node.body = analyze(body_node)
    return True

