import ply.lex as lex

literals = ['+','-','*','/' ]
# Palavras reservadas
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
	'main'		: 'MAIN',
	'true'		: 'TRUE',
	'false'		: 'FALSE'
}

# Nome dos tokens
tokens = ['NUM', 'PLUS', 'MINUS', 'MULT', 'DIV', 'MOD', 'LPAREN', 'RPAREN',
		'LBRAC', 'RBRAC', 'LCBRAC', 'RCBRAC', 'COLON', 'SCOLON', 'COMMA',
		'QMARK', 'NOT', 'AND', 'OR', 'GREATER', 'EQUAL', 'LESS', 'ATTR', 
		'DIFF','LESSEQ', 'GREATEQ', 'AVALPLUS', 'AVALMINUS',
		'AVALMULT', 'AVALDIV', 'AVALMOD', 'ID'] + list(reserved.values())

# Expressao regular dos tokens simples
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
# Ignorando espacos, tabs e comentarios
t_ignore 			= ' \t'
t_ignore_COMMENT	= r'(\/\*(.|\n)*\*\/)|(\/\/.*)'

# Expressao regular com mais regras
def t_NUM(t):
	r'\d+'
	t.value = int(t.value)
	return t

# Regra pra controle de numero de linha
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
	print("Caracter ilegal '%s'" % t.value[0])
	print("Linha: " + repr(t.lineno) + " Coluna: " + repr(find_column(teste, t)) + '\n')
	t.lexer.skip(1)

def t_ID(t):
	r'[a-zA-Z_][a-zA-Z_0-9]*'
	t.type = reserved.get(t.value, 'ID')
	return t

lexer = lex.lex()

# teste = '''
#  a = 5;
# '''

# teste2 = '''
# 3 + 4 * 10 { .
#   + -20 *2 ^
#   _t if (5 >= ab) then
#   else b = 3
#   // comentario
#   teste
#   /* oi
#   3 + 5 */
# }
# '''

#lexer.input(teste)

# print("Teste " + teste)

# while True:
# 	tok = lexer.token()
# 	if not tok:
# 		break
# 	print(tok)
# 	print('Tipo: '+ repr(tok.type)+ 
# 		', Valor: '+ repr(tok.value)+ 
# 		', Linha: '+ repr(tok.lineno)+ 
# 		', Coluna: '+ repr(find_column(teste, tok)) + '\n')