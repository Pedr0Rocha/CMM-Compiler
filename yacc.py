import ply.yacc as yacc
import lex

tokens = lex.tokens

class TreeNode():
    """docstring for TreeNode"""
    def __init__(self, data, children):
        self.data = data;
        self.children = children;

def p_program(p):
    'program : decSeq'
    p[0] = ('program', p[1]);

def p_dec(p):
    '''dec : varDec
           | decFunc
           | decProc'''
    p[0] = p[1];

def p_decFunc(p):
    'decFunc : type ID LPAREN paramList RPAREN LCBRAC block RCBRAC'
    p[0] = ('decFunc', [p[4], p[7]]);

def p_decProc(p):
    'decProc : ID LPAREN paramList RPAREN LCBRAC block RCBRAC'
    p[0] = ('decProc', [p[3], p[6]]);

def p_varDec(p):
    'varDec : type varSpecSeq SCOLON'
    p[0] = ('varDec', [p[1], p[2]]);

def p_varSpec(p):
    '''varSpec : ID
               | ID ATTR literal
               | ID LBRAC num RBRAC
               | ID LBRAC num RBRAC ATTR LCBRAC literalSeq RCBRAC'''
    if len(p) == 2:
        p[0] = p[1];
    elif len(p) == 4:
        p[0] = ('varSpec', [p[1], p[3]]);
    elif len(p) == 5:
        p[0] = ('varSpecArray', [p[1], p[3]]);
    elif len(p) == 6:
        p[0] = ('varSpecArrayAssigned', [p[1], p[3], p[7]]);

def p_varSpecSeq(p):
    '''varSpecSeq : varSpec COMMA varSpecSeq
                  | varSpec'''
    if len(p) == 4:
        p[0] = ('varSpecSeq', [p[1], p[3]]);
    else:
        p[0] = p[1];

def p_paramList(p):
    'paramList : '
    pass

def p_block(p):
    'block : '
    pass

def p_literal(p):
    'literal : num'
    p[0] = p[1];
    
def p_lirealSeq(p):
    'literalSeq : '
    pass

def p_type(p):
    '''type : INT
            | STRING
            | BOOL'''
    p[0] = p[1];

def p_decSeq(p):
    '''decSeq : dec decSeq
              | dec'''
    if len(p) == 3:
        p[0] = ('decSeq', [p[1], p[2]]);
    else: 
        p[0] = p[1]; 

def p_empty(p):
    'empty :'
    pass

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

def p_binop(p):
    '''binop : num PLUS num
             | num MINUS num
             | num DIV num
             | num MULT num'''
    p[0] = (p[2], [p[1], p[3]]);

def p_num(p):
    'num : NUM'
    p[0] = p[1];

teste = '''
 int a = 5;
'''

parser = yacc.yacc()
print parser.parse(teste)
