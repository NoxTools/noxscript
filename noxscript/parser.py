from pyparsing import *
ParserElement.enablePackrat()
from .ast import *

# increase the recursion limit
import sys
sys.setrecursionlimit(5000)

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
_expr = infixNotation(operand,
        [
            (oneOf('- ! ~'), 1, opAssoc.RIGHT, UnOpNode.from_tokens),
            (oneOf('* / %'), 2, opAssoc.LEFT, BinOpNode.from_tokens),
            (oneOf('+ -'), 2, opAssoc.LEFT, BinOpNode.from_tokens),
            (oneOf('<< >>'), 2, opAssoc.LEFT, BinOpNode.from_tokens),
            (~Literal('&&') + '&', 2, opAssoc.LEFT, BinOpNode.from_tokens),
            (oneOf('^'), 2, opAssoc.LEFT, BinOpNode.from_tokens),
            (~Literal('||') + '|', 2, opAssoc.LEFT, BinOpNode.from_tokens),
            (oneOf('< <= > >='), 2, opAssoc.LEFT, BinOpNode.from_tokens),
            (oneOf('== !='), 2, opAssoc.LEFT, BinOpNode.from_tokens),
            (oneOf('&&'), 2, opAssoc.LEFT, BinOpNode.from_tokens),
            (oneOf('||'), 2, opAssoc.LEFT, BinOpNode.from_tokens),
#            (oneOf('|| && * / % + - << >> & | ^ < <= > >= == !='), 2, opAssoc.LEFT, BinOpNode.from_tokens),
            (oneOf('= += -= *= /= %= <<= >>='), 2, opAssoc.RIGHT, AssignNode.from_tokens_op),
        ])
expr = (operand + ~(Optional(White()) + oneOf('- ! ~ * / % + - << >> && || & | < <= > >= == != = += -= *= /= %= <<= >>='))) | _expr
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

#grammar = (func | (vardecl + SEMICOLON) | (assign + SEMICOLON)).ignore(cppStyleComment)

grammar = ZeroOrMore(func | (vardecl + SEMICOLON) | (assign + SEMICOLON))
grammar.ignore(cppStyleComment)

grammar.setParseAction(GlobalNode.from_tokens)

def gen_ast(code):
    root = grammar.parseString(code, True)[0]
    return root
#    root = GlobalNode([])
#
#    loc, node = grammar._parse(code, 0)
#    while node is not None:
#        print node
#        root.children.append(node)
#        if regex
#        loc, node = grammar._parse(code, loc)
#    print loc, root

