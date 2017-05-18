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

def p_decFunc_error(p):
    'decFunc : type ID LPAREN error RPAREN LCBRAC block RCBRAC'
    print("Syntax error at Function Declaration. Bad parameters! Line: " + repr(p.lineno));

def p_decFunc_error2(p):
    'decFunc : type ID LPAREN paramList RPAREN LCBRAC error RCBRAC'
    print("Syntax error at Function Declaration. Bad block! Line: " + repr(p.lineno));

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

def p_literalSeq(p):
    '''literalSeq : literal COMMA literalSeq
                  | literal'''
    if len(p) == 3:
        p[0] = ('literalSeq', [p[1], p[3]]);
    else:
        p[0] = p[1];

def p_paramList(p):
    '''paramList : paramSeq
                 | empty'''
    p[0] = p[1];

def p_param(p):
    '''param : type ID
             | type ID LBRAC RBRAC'''
    p[0] = ('param', [p[1], p[2]]);

def p_block(p):
    'block : varDecList stmtList'
    p[0] = ('block', [p[1], p[2]]);

def p_varDecList(p):
    '''varDecList : varDec varDecList
                  | empty'''
    if len(p) == 3:
        p[0] = ('varDecList', [p[1], p[2]]);
    else:
        p[0] = p[1];

def p_var(p):
    '''var : ID
           | ID LBRAC exp RBRAC'''
    if len(p) == 2:
        p[0] = p[1];
    else:
        p[0] = ('varArray', [p[1], p[3]]);

def p_exp(p):
    '''exp : exp PLUS exp
           | exp MINUS exp
           | exp MULT exp
           | exp DIV exp
           | exp MOD exp
           | exp EQUAL exp
           | exp DIFF exp
           | exp LESSEQ exp
           | exp GREATEQ exp
           | exp GREATER exp
           | exp LESS exp
           | exp AND exp
           | exp OR exp
           | NOT exp
           | exp QMARK exp COLON exp
           | subCall
           | var
           | literal
           | LPAREN exp RPAREN'''
    if len(p) == 4:
        if p[1] != '(':
            p[0] = (p[2], [p[1], p[3]]);
        else:
            p[0] = p[2];
    elif len(p) == 3:
        p[0] = ('NOT', [p[2]]);
    elif len(p) == 6:
        p[0] = ('TERNARYIF', [p[1], p[3], p[5]]);
    else:
        p[0] = p[1];


def p_stmt(p):
    '''stmt : ifStmt
            | whileStmt
            | forStmt
            | breakStmt
            | returnStmt
            | readStmt
            | writeStmt
            | assign SCOLON
            | subCall SCOLON'''
    p[0] = p[1];

def p_ifStmt(p):
    '''ifStmt : IF LPAREN exp RPAREN LCBRAC block RCBRAC
              | IF LPAREN exp RPAREN LCBRAC block RCBRAC ELSE RCBRAC block LCBRAC'''
    if len(p) == 8:
        p[0] = ('if', [p[3], p[6]]);
    else:
        p[0] = ('ifelse', [p[3], p[6], p[10]]);

def p_whileStmt(p):
    'whileStmt : WHILE LPAREN exp RPAREN LCBRAC block RCBRAC'
    p[0] = ('while', [p[3], p[6]]);

def p_forStmt(p):
    'forStmt : FOR LPAREN assign SCOLON exp SCOLON assign RPAREN LCBRAC block RCBRAC'
    p[0] = ('for', [p[3], p[5], p[7], p[10]]);

def p_breakStmt(p):
    'breakStmt : BREAK SCOLON'
    p[0] = p[1];

def p_returnStmt(p):
    '''returnStmt : RETURN SCOLON
                  | RETURN exp SCOLON'''
    if len(p) == 3:
        p[0] = p[1];
    else:
        p[0] = ('return', p[2]);

def p_returnStmt_error(p):
    '''returnStmt : RETURN error SCOLON'''
    print("Syntax error at Return Statement. Line: " + repr(p.lineno));

def p_readStmt(p):
    'readStmt : READ var SCOLON'
    p[0] = ('read', [p[2]]);

def p_writeStmt(p):
    'writeStmt : WRITE expList SCOLON'
    p[0] = ('write', [p[2]]);

def p_assign(p):
    '''assign : var ATTR exp
              | var AVALPLUS exp
              | var AVALMINUS exp
              | var AVALMULT exp
              | var AVALDIV exp
              | var AVALMOD exp'''
    p[0] = (p[2], [p[1], p[3]]);

def p_subCall(p):
    'subCall : ID LPAREN expList RPAREN'
    p[0] = ('subCall', [p[1], p[3]]);

def p_expList(p):
    '''expList : expSeq
               | empty'''
    p[0] = p[1];

def p_expSeq(p):
    '''expSeq : exp COMMA expSeq
              | exp'''
    if len(p) == 4:
        p[0] = ('expSeq', [p[1], p[3]]);
    else:
        p[0] = p[1];

def p_stmtList(p):
    '''stmtList : stmt stmtList
                | empty'''
    if len(p) == 3:
        p[0] = ('stmtList', [p[1], p[2]]);
    else:
        p[0] = p[1];    

def p_literal(p):
    '''literal : num
               | str
               | logic'''
    p[0] = p[1];

def p_num(p):
    'num : NUM'
    p[0] = p[1];

def p_str(p):
    'str : STR'
    p[0] = p[1];

def p_logic(p):
    '''logic : TRUE
             | FALSE'''
    p[0] = p[1];
    
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

def p_paramSeq(p):
    '''paramSeq : param COMMA paramSeq
                | param'''
    if len(p) == 4:
        p[0] = ('paramSeq', [p[1], p[3]]);
    else: 
        p[0] = p[1]; 

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
         print("Syntax error at token", p)
    else:
         print("Syntax error at EOF")

teste = '''
    int v[10];
    /*
        Procedimento de ordenacao por troca
        Observe como um parametro de arranjo e declarado
    */
    bubblesort(int v[], int n) {
        int i=0, j;
        bool trocou = true;
        while (i < n-1 && trocou) {
            trocou = false;
            for (j=0; j < n-i-1; j+=1) {
                if (v[j] > v[j+1]) {
                    int aux;
                    aux = v[j];
                    v[j] = v[j+1];
                    v[j+1] = aux;
                    trocou = true;
                }
            }
            i += 1;
        }
    }

    main() {
        int i;
        for (i=0; i < 10; i+=1) {
            read v[i];
        }
        bubblesort(v, 10);
        for (i=0; i < 10; i+=1) {
            write v[i], " ";
        }
    }
'''

parser = yacc.yacc()
print parser.parse(teste)
