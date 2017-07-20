import ply.lex as lex
from test import test

reserved = {
	'if'		: 'IF',
	'then'		: 'THEN',
	'else'		: 'ELSE',
	'for'		: 'FOR',
	'while'		: 'WHILE',
	'break'		: 'BREAK',
	'return'	: 'RETURN',
	'function'	: 'FUNCTION',
	'void'		: 'VOID',
	'int'		: 'INT',
	'bool'		: 'BOOL',
	'string'	: 'STRING',
	'true'		: 'TRUE',
	'false'		: 'FALSE',
	'read'		: 'READ',
	'write'		: 'WRITE'
}

tokens = ['NUM', 'PLUS', 'MINUS', 'MULT', 'DIV', 'MOD', 'LPAREN', 'RPAREN',
		'LBRAC', 'RBRAC', 'LCBRAC', 'RCBRAC', 'COLON', 'SCOLON', 'COMMA',
		'QMARK', 'NOT', 'AND', 'OR', 'GREATER', 'EQUAL', 'LESS', 'ATTR', 
		'DIFF','LESSEQ', 'GREATEQ', 'AVALPLUS', 'AVALMINUS',
		'AVALMULT', 'AVALDIV', 'AVALMOD', 'ID', 'STR'] + list(reserved.values())

t_PLUS		= r'\+'
t_MINUS 	= r'-'
t_MULT		= r'\*'
t_DIV		= r'/'
t_MOD		= r'%'
t_LPAREN	= r'\('
t_RPAREN	= r'\)'
t_LBRAC		= r'\['
t_RBRAC		= r'\]'
t_LCBRAC	= r'{'
t_RCBRAC	= r'}'
t_COLON		= r':'
t_SCOLON	= r';'
t_COMMA		= r','
t_QMARK		= r'\?'
t_NOT		= r'!'
t_AND		= r'&&'
t_OR 		= r'\|\|'
t_GREATER	= r'>'
t_EQUAL		= r'=='
t_LESS		= r'<'
t_ATTR		= r'='
t_DIFF		= r'!='
t_LESSEQ	= r'<='
t_GREATEQ	= r'>='
t_AVALPLUS	= r'\+='
t_AVALMINUS	= r'-='
t_AVALMULT	= r'\*='
t_AVALDIV	= r'/='
t_AVALMOD	= r'%='
t_STR		= r'\"(\\.|[^"])*\"'
# Ignoring spaces, tabs and comments
t_ignore 			= ' \t'
t_ignore_COMMENT	= r'(\/\*(.|\n)*\*\/)|(\/\/.*)'

def t_NUM(t):
	r'\d+'
	t.value = int(t.value)
	return t

def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

def find_column(input,token):
    last_cr = input.rfind('\n',0,token.lexpos)
    if last_cr < 0:
	last_cr = 0
    column = (token.lexpos - last_cr) + 1
    return column

def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	print("Line: " + repr(t.lineno) + " Column: " + repr(find_column(teste, t)) + '\n')
	t.lexer.skip(1)

def t_ID(t):
	r'[a-zA-Z_][a-zA-Z_0-9]*'
	t.type = reserved.get(t.value, 'ID')
	return t

lexer = lex.lex()

lexer.input(test)

print("Test " + test)


print "\n\nLexer Analysis\n\n";
while True:
    tok = lexer.token()
    last_cr = lex.lexer.lexdata.rfind('\n', 0, lex.lexer.lexpos)
    column = lex.lexer.lexpos - last_cr - 1
    if not tok:
        break
    lexToken = 'LexToken(Token: %s, Value: %r, Line: %d, Column: %d)' % (tok.type, tok.value, tok.lineno, column)
    print (lexToken)