from pyparsing import *
ParserElement.enablePackrat()
from .ast import *

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
expr = infixNotation(arrexpr | funccall | true | false | self | other | Group(name).setParseAction(VarNode.from_tokens) | literal,
        [
            ('-', 1, opAssoc.RIGHT, UnOpNode.from_tokens),
            (oneOf('* / %'), 2, opAssoc.LEFT, BinOpNode.from_tokens),
            (oneOf('+ -'), 2, opAssoc.LEFT, BinOpNode.from_tokens),
            (oneOf('<< >>'), 2, opAssoc.LEFT, BinOpNode.from_tokens),
            (oneOf('&'), 2, opAssoc.LEFT, BinOpNode.from_tokens),
            (oneOf('^'), 2, opAssoc.LEFT, BinOpNode.from_tokens),
            (oneOf('|'), 2, opAssoc.LEFT, BinOpNode.from_tokens),
            (oneOf('< <= > >='), 2, opAssoc.LEFT, BinOpNode.from_tokens),
            (oneOf('== !='), 2, opAssoc.LEFT, BinOpNode.from_tokens),
            (oneOf('&&'), 2, opAssoc.LEFT, BinOpNode.from_tokens),
            (oneOf('||'), 2, opAssoc.LEFT, BinOpNode.from_tokens),
            (oneOf('= += -= *= /= %='), 2, opAssoc.RIGHT, AssignNode.from_tokens_op),
            #(oneOf(','), 2, opAssoc.LEFT),
        ])
args = Optional(expr + ZeroOrMore(Suppress(Literal(',')) + expr))
funccall << (name + LPAREN + args + RPAREN)
funccall.setParseAction(CallNode.from_tokens)
arrexpr << (name + LBRAC + expr + RBRAC)
arrexpr.setParseAction(SubscriptNode.from_tokens)
assign = (vartype + name + Suppress(Literal('=')) + expr).setParseAction(AssignNode.from_tokens)
blockstmt = Forward()
ifstmt = Forward()
whilestmt = Forward()
forstmt = Forward()
label = (Suppress(LineEnd()) + name + Suppress(Literal(':'))).setParseAction(LabelNode.from_tokens)
goto = (Suppress(Keyword('goto')) + name).setParseAction(GotoNode.from_tokens)
retstmt = (Suppress(Keyword('return')) + Optional(expr)).setParseAction(ReturnNode.from_tokens)
statement = Optional(label) + (blockstmt | ifstmt | whilestmt | forstmt | ((
    retstmt  |
    Keyword('continue').setParseAction(ContinueNode.from_tokens) |
    Keyword('break').setParseAction(BreakNode.from_tokens) |
    goto |
    assign |
    vardecl |
    expr
    ) + SEMICOLON))
blockstmt << Suppress(Literal('{')) + Group(ZeroOrMore(statement)) + Suppress(Literal('}'))
blockstmt.setParseAction(BlockNode.from_tokens)
elsestmt = Suppress(Keyword('else')) + statement
ifstmt << (Suppress(Keyword('if')) + LPAREN + expr + RPAREN + statement + Optional(elsestmt))
ifstmt.setParseAction(IfNode.from_tokens)
whilestmt << (Suppress(Keyword('while')) + LPAREN + expr + RPAREN + statement)
whilestmt.setParseAction(WhileNode.from_tokens)
forstmt << (Suppress(Keyword('for')) + LPAREN + Optional(expr, None) + SEMICOLON +
                 Optional(expr, None) + SEMICOLON +
                 Optional(expr, None) + RPAREN + statement)
forstmt.setParseAction(ForNode.from_tokens)
argdecl = (vartype + name).setParseAction(DeclNode.from_tokens)
funcdecl = (Keyword('void') | vartype) + name + LPAREN + Optional(argdecl + ZeroOrMore(Suppress(Literal(',')) + argdecl)) + RPAREN
func = (funcdecl + statement).setParseAction(FuncNode.from_tokens)

grammar = ZeroOrMore(func | (vardecl + SEMICOLON))
grammar.ignore(cppStyleComment)

grammar.setParseAction(GlobalNode.from_tokens)

def gen_ast(code):
    root = grammar.parseString(code, True)[0]
    return root

