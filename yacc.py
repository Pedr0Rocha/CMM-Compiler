import ply.yacc as yacc
from test import test
import lex
import ast 
import helpers

tokens = lex.tokens
lex.lexer.lineno = 1;

precedence = (
    ('left', 'MULT', 'DIV', 'MOD'),
    ('left', 'PLUS', 'MINUS'),
    ('right', 'NOT'),
    ('left', 'GREATEQ', 'LESSEQ', 'GREATER', 'LESS'),
    ('left', 'EQUAL', 'DIFF'),
    ('left', 'AND'),
    ('left', 'OR'),
    ('right', 'QMARK')
);

def p_program(p):
    'program : decSeq'
    p[0] = ast.ProgramTreeNode({
            'program' : p[1],
        });

def p_dec(p):
    '''dec : varDec
           | decFunc
           | decProc'''
    p[0] = p[1];

def p_decFunc(p):
    'decFunc : type ID LPAREN paramList RPAREN LCBRAC block RCBRAC'
    p[0] = ast.DecFuncTreeNode({
            'type'      : p[1],
            'id'        : p[2],
            'paramList' : p[4],
            'block'     : p[7],
            'pos'       : { 'line' : p.lineno(2), 'column' : getColumn() },
        });

def p_decProc(p):
    'decProc : ID LPAREN paramList RPAREN LCBRAC block RCBRAC'
    p[0] = ast.DecProcTreeNode({
            'id'        : p[1],
            'paramList' : p[3],
            'block'     : p[6],
            'pos'       : { 'line' : p.lineno(1), 'column' : getColumn() },
        });

def p_varDec(p):
    'varDec : type varSpecSeq SCOLON'
    p[0] = ast.VarDecTreeNode({
            'type'       : p[1],
            'varSpecSeq' : p[2],
            'pos'        : { 'line' : p.lineno(3), 'column' : getColumn() },
        });

def p_varSpec(p):
    '''varSpec : ID
               | ID ATTR literal
               | ID LBRAC num RBRAC
               | ID LBRAC num RBRAC ATTR LCBRAC literalSeq RCBRAC'''
    if len(p) == 2:
        p[0] = ast.VarTreeNode({
                'id'  : p[1],
                'pos' : { 'line' : p.lineno(1), 'column' : getColumn() },
            });
    elif len(p) == 4:
        p[0] = ast.VarTreeNode({
                'id'      : p[1],
                'literal' : p[3],
                'pos'     : { 'line' : p.lineno(1), 'column' : getColumn() },
            });
    elif len(p) == 5:
        p[0] = ast.VarTreeNode({
                'id'   : p[1],
                'size' : p[3],
                'pos'  : { 'line' : p.lineno(1), 'column' : getColumn() },
            });
    elif len(p) == 6:
        p[0] = ast.VarTreeNode({
                'id'         : p[1],
                'size'       : p[3],
                'literalSeq' : p[7],
                'pos'        : { 'line' : p.lineno(1), 'column' : getColumn() },
            });

def p_varSpecSeq(p):
    '''varSpecSeq : varSpec COMMA varSpecSeq
                  | varSpec'''
    if len(p) == 4:
        p[0] = ast.VarSeqTreeNode({
                'var'    : p[1],
                'varSeq' : p[3],
            });
    else:
        p[0] = ast.VarSeqTreeNode({
                'var'    : p[1],
            });

def p_literalSeq(p):
    '''literalSeq : literal COMMA literalSeq
                  | literal'''
    if len(p) == 4:
        p[0] = ast.LiteralSeqTreeNode({
                'lit'    : p[1],
                'litSeq' : p[3],
            });
    else:
        p[0] = ast.LiteralSeqTreeNode({
                'lit' : p[1],
            });

def p_paramList(p):
    '''paramList : paramSeq
                 | empty'''
    p[0] = p[1];

def p_param(p):
    '''param : type ID
             | type ID LBRAC RBRAC'''
    p[0] = ast.ParamTreeNode({
            'type'     : p[1],
            'id'       : p[2],
            'isVector' : len(p) == 5,
        });

def p_block(p):
    'block : varDecList stmtList'
    p[0] = ast.BlockTreeNode({
            'varDecList' : p[1],
            'stmtList'   : p[2],
        });

def p_varDecList(p):
    '''varDecList : varDec varDecList
                  | empty'''
    if len(p) == 3:
        p[0] = ast.VarDecListTreeNode({
                'varDec'     : p[1],
                'varDecList' : p[2],
            });
    else:
        p[0] = p[1];

def p_var(p):
    '''var : ID
           | ID LBRAC exp RBRAC'''
    if len(p) == 2:
        p[0] = ast.IDTreeNode({
                'id'  : p[1],
                'pos' : { 'line' : p.lineno(1), 'column' : getColumn() },
            });
    else:
        p[0] = ast.IDVectorTreeNode({
                'id'  : p[1],
                'exp' : p[3],
                'pos' : { 'line' : p.lineno(1), 'column' : getColumn() },
            });

def p_exp(p):
    '''exp : binop
           | NOT exp
           | exp QMARK exp COLON exp
           | subCall
           | var
           | literal
           | LPAREN exp RPAREN'''
    if len(p) == 4:
            p[0] = p[2];
    elif len(p) == 3:
        p[0] = ast.ExpressionTreeNode({
                'op'  : 'not',
                'exp' : p[2],
                'pos' : { 'line' : p.lineno(1), 'column' : getColumn() },
            });
    elif len(p) == 6:
        p[0] = ast.ExpressionTreeNode({
                'op'        : 'ternaryif',
                'expIf'     : p[1],
                'expThen'   : p[3],
                'expElse'   : p[5],
                'pos'       : { 'line' : p.lineno(2), 'column' : getColumn() },
            });
    else:
        p[0] = p[1];

def p_binop(p):
    '''binop : exp PLUS exp
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
             | exp OR exp'''
    p[0] = ast.BinopTreeNode({ 
            'op'   : p[2], 
            'left' : p[1], 
            'right': p[3], 
            'pos'  : { 'line' : p.lineno(2), 'column' : getColumn() },
        });

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
        p[0] = ast.IfTreeNode({
                'exp'   : p[3],
                'block' : p[6],
                'pos'   : { 'line' : p.lineno(1), 'column' : getColumn() },
            });
    else:
        p[0] = ast.IfElseTreeNode({
                'exp'       : p[3],
                'block'     : p[6],
                'blockElse' : p[10], 
                'pos'       : { 'line' : p.lineno(1), 'column' : getColumn() },
            });

def p_whileStmt(p):
    'whileStmt : WHILE LPAREN exp RPAREN LCBRAC block RCBRAC'
    p[0] = ast.WhileTreeNode({
            'exp'   : p[3],
            'block' : p[6],
            'pos'   : { 'line' : p.lineno(1), 'column' : getColumn() },
        });

def p_forStmt(p):
    'forStmt : FOR LPAREN assign SCOLON exp SCOLON assign RPAREN LCBRAC block RCBRAC'
    p[0] = ast.ForTreeNode({
            'assignInit' : p[3],
            'exp' : p[5],
            'assignEnd' : p[7],
            'block' : p[10],
            'pos' : { 'line' : p.lineno(1), 'column' : getColumn() },
        });

def p_breakStmt(p):
    'breakStmt : BREAK SCOLON'
    p[0] = ast.BreakTreeNode({
            'pos' : { 'line' : p.lineno(1), 'column' : getColumn() },
        });

def p_returnStmt(p):
    '''returnStmt : RETURN SCOLON
                  | RETURN exp SCOLON'''
    if len(p) == 3:
        p[0] = ast.ReturnTreeNode({
                'pos' : { 'line' : p.lineno(1), 'column' : getColumn() },
            });
    else:
        p[0] = ast.ReturnTreeNode({
                'exp' : p[2],
                'pos' : { 'line' : p.lineno(1), 'column' : getColumn() },
            });

def p_readStmt(p):
    'readStmt : READ var SCOLON'
    p[0] = ast.ReadTreeNode({
            'var' : p[2],
            'pos' : { 'line' : p.lineno(1), 'column' : getColumn() },
        });

def p_writeStmt(p):
    'writeStmt : WRITE expList SCOLON'
    p[0] = ast.WriteTreeNode({
            'expList' : p[2],
            'pos' : { 'line' : p.lineno(1), 'column' : getColumn() },
        });

def p_assign(p):
    '''assign : var ATTR exp
              | var AVALPLUS exp
              | var AVALMINUS exp
              | var AVALMULT exp
              | var AVALDIV exp
              | var AVALMOD exp'''
    p[0] = ast.AssignTreeNode({
            'var' : p[1],
            'op'  : p[2],
            'exp' : p[3],
            'pos' : { 'line' : p.lineno(2), 'column' : getColumn() },
        });

def p_subCall(p):
    'subCall : ID LPAREN expList RPAREN'
    p[0] = ast.SubCallTreeNode({
            'id'      : p[1],
            'expList' : p[3],
            'pos'     : { 'line' : p.lineno(1), 'column' : getColumn() },
        });

def p_expList(p):
    '''expList : expSeq
               | empty'''
    p[0] = p[1];

def p_expSeq(p):
    '''expSeq : exp COMMA expSeq
              | exp'''
    if len(p) == 4:
        p[0] = ast.ExpSeqTreeNode({
                'exp'    : p[1],
                'expSeq' : p[3],
            });
    else:
        p[0] = ast.ExpSeqTreeNode({
                'exp' : p[1],
            });

def p_stmtList(p):
    '''stmtList : stmt stmtList
                | empty'''
    if len(p) == 3:
        p[0] = ast.StmtListTreeNode({
                'stmt'     : p[1],
                'stmtList' : p[2],
            });
    else:
        p[0] = p[1];

def p_literal(p):
    '''literal : num
               | str
               | logic'''
    p[0] = p[1];

def p_num(p):
    'num : NUM'
    p[0] = ast.NumTreeNode({
            'value' : p[1],
        });
 
def p_str(p):
    'str : STR'
    p[0] = ast.StrTreeNode({
            'value' : p[1],
        });

def p_logic(p):
    '''logic : TRUE
             | FALSE'''
    #p[0] = p[1];
    p[0] = ast.LogicTreeNode({
            'value' : p[1],
        });
    
def p_type(p):
    '''type : INT
            | STRING
            | BOOL'''
    p[0] = p[1];

def p_decSeq(p):
    '''decSeq : dec decSeq
              | dec'''
    if len(p) == 3:
        p[0] = ast.DecSeqTreeNode({
                'dec'    : p[1],
                'decSeq' : p[2],
            });
    else: 
        p[0] = ast.DecSeqTreeNode({
                'dec' : p[1],
            });

def p_paramSeq(p):
    '''paramSeq : param COMMA paramSeq
                | param'''
    if len(p) == 4:
        p[0] = ast.ParamSeqTreeNode({
                'param'    : p[1],
                'paramSeq' : p[3],
            });
    else: 
        p[0] = ast.ParamSeqTreeNode({
                'param' : p[1],
            });

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print "Syntax error at " + str(p.lineno) + ", " + str(getColumn()) + " - token " + str(p.value);
    else:
        print "Syntax error at EOF";


def getColumn():
    last_cr = lex.lexer.lexdata.rfind('\n', 0, lex.lexer.lexpos);
    column = lex.lexer.lexpos - last_cr - 1;
    return column;

print "\n\n====== Syntax Analysis ======\n\n";
parser = yacc.yacc()
root = parser.parse(test)

print "\n\n====== Semantic Analysis ======\n\n";
root.evaluate();
#root.printNode();
