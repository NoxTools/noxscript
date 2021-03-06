from cPickle import dump, load
from hashlib import md5
from io import BytesIO, BufferedReader, FileIO
from pycparser import c_parser, c_ast, parse_file

BUILTINS = {}

class FuncDeclVisitor(c_ast.NodeVisitor):
    def visit_Decl(self, node):
        if isinstance(node.type, c_ast.FuncDecl):
            BUILTINS[node.name] = {
                'num': len(BUILTINS),
                'name': node.name,
                'rettype': node.type.type.type.names[0],
                'args': [{'type': x.type.type.names[0], 'name': x.name} for x in node.type.args.params] if node.type.args else []
            }

with open('builtins.h', 'rb') as f:
    digest = md5(f.read()).hexdigest()
try:
    with open('builtins.pickle', 'rb') as f:
        cache = load(f)
        if cache and cache['md5'] == digest:
            BUILTINS = cache['builtins']
except EOFError:
    pass
except IOError:
    pass

if len(BUILTINS) == 0:
    # pycparser doesn't handle comments
    # so we need to strip them out beforehand
    inp = BufferedReader(FileIO('builtins.h'))
    tmp = BytesIO()

    lastch = None
    in_comment = False
    while True:
        ch = inp.read(1)
        if len(ch) == 0:
            break
        if not in_comment and lastch == '/' and ch == '*':
            in_comment = True
            tmp.seek(-1, 1)
        elif in_comment and lastch == '*' and ch == '/':
            in_comment = False
        elif not in_comment:
            tmp.write(ch)
        lastch = ch
    tmp.truncate()

    parser = c_parser.CParser()
    ast = parser.parse(tmp.getvalue(), 'builtins.h')
    v = FuncDeclVisitor()
    v.visit(ast)

    inp.close()
    tmp.close()

    with open('builtins.pickle', 'wb') as f:
        dump({'md5': digest, 'builtins': BUILTINS}, f)
