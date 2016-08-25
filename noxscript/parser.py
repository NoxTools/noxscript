from pyparsing import *
from .ast import *

# increase the recursion limit
import sys
sys.setrecursionlimit(5000)
OP_MAP = {
    '#': (1, opAssoc.RIGHT, UnOpNode.from_tokens, 0),
    '!': (1, opAssoc.RIGHT, UnOpNode.from_tokens, 0),
    '~': (1, opAssoc.RIGHT, UnOpNode.from_tokens, 0),

    '*': (2, opAssoc.LEFT, BinOpNode.from_tokens, 1),
    '/': (2, opAssoc.LEFT, BinOpNode.from_tokens, 1),
    '%': (2, opAssoc.LEFT, BinOpNode.from_tokens, 1),

    '-': (2, opAssoc.LEFT, BinOpNode.from_tokens, 2),
    '+': (2, opAssoc.LEFT, BinOpNode.from_tokens, 2),

    '<<': (2, opAssoc.LEFT, BinOpNode.from_tokens, 3),
    '>>': (2, opAssoc.LEFT, BinOpNode.from_tokens, 3),

    '&': (2, opAssoc.LEFT, BinOpNode.from_tokens, 4),
    '^': (2, opAssoc.LEFT, BinOpNode.from_tokens, 5),
    '|': (2, opAssoc.LEFT, BinOpNode.from_tokens, 6),

    '<': (2, opAssoc.LEFT, BinOpNode.from_tokens, 7),
    '<=': (2, opAssoc.LEFT, BinOpNode.from_tokens, 7),
    '>': (2, opAssoc.LEFT, BinOpNode.from_tokens, 7),
    '>=': (2, opAssoc.LEFT, BinOpNode.from_tokens, 7),

    '==': (2, opAssoc.LEFT, BinOpNode.from_tokens, 8),
    '!=': (2, opAssoc.LEFT, BinOpNode.from_tokens, 8),

    '&&': (2, opAssoc.LEFT, BinOpNode.from_tokens, 9),
    '||': (2, opAssoc.LEFT, BinOpNode.from_tokens, 10),

    '=': (2, opAssoc.RIGHT, AssignNode.from_tokens_op, 11),
    '+=': (2, opAssoc.RIGHT, AssignNode.from_tokens_op, 11),
    '-=': (2, opAssoc.RIGHT, AssignNode.from_tokens_op, 11),
    '*=': (2, opAssoc.RIGHT, AssignNode.from_tokens_op, 11),
    '/=': (2, opAssoc.RIGHT, AssignNode.from_tokens_op, 11),
    '%=': (2, opAssoc.RIGHT, AssignNode.from_tokens_op, 11),
    '<<=': (2, opAssoc.RIGHT, AssignNode.from_tokens_op, 11),
    '>>=': (2, opAssoc.RIGHT, AssignNode.from_tokens_op, 11),
}

class Operator(object):
    def __init__( self, loc, tokens ):
        self.loc = loc
        self.op = tokens[0]

class OperatorPrecedence(ParseExpression):
    def __init__( self, operand, savelist = False ):
        self.operands = Optional(oneOf('-= - != ! ~ *= * /= / %= % += + <<= << >>= >> && || & | <= < >= > == != = += -= *= /= %= <<= >>= ( )').setParseAction(lambda loc, tok: Operator(loc, tok)))

        super(OperatorPrecedence,self).__init__([operand], savelist)

    def parseImpl( self, instring, loc, doActions=True ):
        lastError = None
        queue = []
        op_stack = []
        expr = self.exprs[0]
        lastTok = None
        assert doActions
        while True:
            old_loc = loc
            loc, tokens = self.operands._parse( instring, loc, doActions )
            if len(tokens) == 0:
                try:
                    loc, tokens = expr._parse( instring, loc, doActions )
                except ParseException as err:
                    lastError = err
                    break
                except IndexError:
                    lastError = err
                    break

            assert len(tokens) == 1
            tok = tokens[0]
            if isinstance(tok, Operator):
                if tok.op == '(':
                    op_stack.append(tok)
                elif tok.op == ')':
                    error = False
                    while True:
                        if len(op_stack) == 0:
                            error = True
                            break
                        op = op_stack.pop()
                        if op.op == '(':
                            break
                        queue.append(op)
                    if error:
                        loc = old_loc
                        break
                else:
                    tok.count, tok.assoc, tok.action, tok.prec = OP_MAP[tok.op]
                    if tok.op == '-':
                        if lastTok is None or (isinstance(lastTok, Operator) and lastTok.op != ')'):
                            tok.count, tok.assoc, tok.action, tok.prec = OP_MAP['#']
                    if tok.count > 1:
                        while len(op_stack) > 0:
                            op = op_stack[-1]
                            if not isinstance(op, Operator) or op.op == '(' or op.op == ')':
                                break
                            if (tok.assoc == opAssoc.LEFT and tok.prec <= op.prec) or \
                              (tok.assoc == opAssoc.RIGHT and tok.prec < op.prec):
                                queue.append(op_stack.pop())
                            else:
                                break
                    op_stack.append(tok)
            else:
                queue.append(tok)
            lastTok = tok
        while len(op_stack):
            queue.append(op_stack.pop())
        stack = []
        while len(queue) > 0:
            op = queue.pop(0)
            if isinstance(op, Operator):
                if op.count == 1:
                    tok = op.action(instring, op.loc, [[op.op, stack.pop()]])
                    stack.append(tok)
                elif op.count == 2:
                    rhs = stack.pop()
                    lhs = stack.pop()
                    tok = op.action(instring, op.loc, [[lhs, op.op, rhs]])
                    stack.append(tok)
            else:
                stack.append(op)
        if len(stack) > 1:
            raise ParseException(instring, loc, "bad expression", self)

        return loc, stack

LPAREN = Suppress(Literal('('))
RPAREN = Suppress(Literal(')'))
NEG = Literal('-')
SEMICOLON = Suppress(Literal(';'))
LBRAC = Suppress(Literal('['))
RBRAC = Suppress(Literal(']'))

# built-in constants
true = Keyword('true').setParseAction(lambda toks: LiteralNode(1))
false = Keyword('false').setParseAction(lambda toks: LiteralNode(0))
self = Keyword('self').setParseAction(lambda toks: LiteralNode(-1))
other = Keyword('other').setParseAction(lambda toks: LiteralNode(-2))

vartype = Keyword('int') | Keyword('float') | Keyword('string') | Keyword('object')
name = Word(alphas + '_', alphanums + '_', asKeyword=True)
qs = QuotedString('"', escChar='\\')
integer = (Regex(r'0x[0-9a-fA-F]+') | Regex(r'\d+')).setParseAction(lambda toks: int(toks[0], 0))
fp = Regex(r'\d+(\.\d*)([eE]\d+)?').setParseAction(lambda toks: float(toks[0]))
literal = (qs | fp | integer).setParseAction(LiteralNode.from_tokens)
vardecl = (vartype + name + Optional(LBRAC + integer + RBRAC)).setParseAction(DeclNode.from_tokens)
funccall = Forward()
arrexpr = Forward()
operand = arrexpr | funccall | true | false | self | other | Group(name).setParseAction(VarNode.from_tokens) | literal
expr = OperatorPrecedence(operand)
args = Optional(delimitedList(expr))
funccall << (name + LPAREN - args - RPAREN)
funccall.setParseAction(CallNode.from_tokens)
arrexpr << (name + LBRAC - expr - RBRAC)
arrexpr.setParseAction(SubscriptNode.from_tokens)
assign = (vartype + name + Suppress(Literal('=')) - expr).setParseAction(AssignNode.from_tokens)
blockstmt = Forward()
ifstmt = Forward()
whilestmt = Forward()
forstmt = Forward()
label = (name + Suppress(Literal(':'))).setParseAction(LabelNode.from_tokens)
goto = (Suppress(Keyword('goto')) - name).setParseAction(GotoNode.from_tokens)
retstmt = (Suppress(Keyword('return')) - Optional(expr)).setParseAction(ReturnNode.from_tokens)
statement = Optional(label) + (blockstmt | ifstmt | whilestmt | forstmt | ((
    retstmt  |
    Keyword('continue').setParseAction(ContinueNode.from_tokens) |
    Keyword('break').setParseAction(BreakNode.from_tokens) |
    goto |
    assign |
    vardecl |
    expr
    ) + SEMICOLON))
blockstmt << Suppress(Literal('{')) - Group(ZeroOrMore(statement) - Optional(label)) - Suppress(Literal('}'))
blockstmt.setParseAction(BlockNode.from_tokens)
elsestmt = Suppress(Keyword('else')) - statement
ifstmt << (Suppress(Keyword('if')) - LPAREN - expr - RPAREN - statement - Optional(elsestmt))
ifstmt.setParseAction(IfNode.from_tokens)
whilestmt << (Suppress(Keyword('while')) - LPAREN + expr + RPAREN + statement)
whilestmt.setParseAction(WhileNode.from_tokens)
forstmt << (Suppress(Keyword('for')) - LPAREN + Optional(expr, None) + SEMICOLON +
                 Optional(expr, None) + SEMICOLON +
                 Optional(expr, None) + RPAREN + statement)
forstmt.setParseAction(ForNode.from_tokens)
argdecl = (vartype + name).setParseAction(DeclNode.from_tokens)
funcdecl = (Keyword('void') | vartype) + name + LPAREN - Optional(delimitedList(argdecl)) + RPAREN
func = (funcdecl - statement).setParseAction(FuncNode.from_tokens)

grammar = ZeroOrMore(func | (vardecl + SEMICOLON) | (assign + SEMICOLON))
grammar.ignore(cppStyleComment)

grammar.setParseAction(GlobalNode.from_tokens)

def gen_ast(code):
    root = grammar.parseString(code, True)[0]
    return root
