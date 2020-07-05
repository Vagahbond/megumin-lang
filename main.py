import ply.yacc as yacc
import ply.lex as lex
import sys as sys
from genereTreeGraphviz2 import printTreeGraph

reserved = {
    'out': 'PRINT',
    'if': 'IF',
    'else': 'ELSE',
    'end': 'END',
    'while': 'WHILE',
    'until': 'UNTIL',
    'for': 'FOR',
    'let': 'LET',
    'return': 'RETURN'

}


tokens = [
    'NUMBER', 'MINUS',
    'PLUS', 'TIMES', 'DIVIDE',
    'LPAREN', 'RPAREN', 'OR',
    'AND', 'SEMICOLON', 'NAME',
    'AFFECT', 'GT', 'LT',
    'LOE', 'GOE', 'EQUALS', 'DIFFERENT',
    'COR', 'CAND', 'COMMA'
] + list(reserved.values())


# Tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_OR = r'\|'
t_AND = r'\&'
t_SEMICOLON = r';'
t_AFFECT = r'='
t_LT = r'<'
t_GT = r'>'
t_LOE = r'<='
t_GOE = r'>='
t_EQUALS = r'=='
t_DIFFERENT = r'!='
t_COR = r'\|\|'
t_CAND = r'\&\&'
t_COMMA = r','


variables = {}
stack = [{},]
functions = {}


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'NAME')
    return t


# Ignored characters
t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lex.lex()

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right',  'GT', 'LT',
     'LOE', 'GOE', 'EQUALS', 'DIFFERENT'),
    ('right', 'AND', 'OR'),
    ('left', 'AFFECT'),
)


def p_start(p):
    'start : block'
    p[0] = ('START', p[1])
    print('Arbre de derivation = ', p[0])
    #printTreeGraph(p[1])
    evalInst(p[1])


def p_block(p):
    '''block : instruction  block 
    | condition block
    | loop block
    |  funcdef block'''
    p[0] = ('block', p[1], p[2])


def p_block_terminal(p):
    '''block : instruction
    | condition
    | loop
    | funcdef'''
    p[0] = ('block', p[1])


def p_define_void(p):
    'funcdef : LET NAME LPAREN declarg RPAREN  block END'
    p[0] = ('funcdef', p[2], p[4], p[6], None)

def p_define_noparam_void(p):
    'funcdef : LET NAME LPAREN  RPAREN  block END'
    p[0] = ('funcdef', p[2], None, p[5], None)


def p_define_function(p):
    'funcdef : LET NAME LPAREN declarg RPAREN block RETURN expression END'
    p[0] = ('funcdef', p[2], p[4], p[6], p[8])

def p_define_noparam_function(p):
    'funcdef : LET NAME LPAREN RPAREN block RETURN expression END'
    p[0] = ('funcdef', p[2], None, p[5], p[7])



def p_call_void_statement(p):
    'statement : NAME LPAREN callarg RPAREN'
    p[0] = ('voidcall', p[1], p[3])

def p_call_noparam_void_statement(p):
    'statement : NAME LPAREN  RPAREN'
    p[0] = ('voidcall', p[1], None)

def p_call_func_statement(p):
    'expression : NAME LPAREN callarg RPAREN'
    p[0] = ('funccall', p[1], p[3])

def p_call_noparam_func_statement(p):
    'expression : NAME LPAREN  RPAREN'
    p[0] = ('funccall', p[1], None)


def p_declargs(p):
    'declarg : NAME COMMA declarg'
    p[0] = ('declarg', p[1], p[3])


def p_declarg(p):
    'declarg : NAME'
    p[0] = ('declarg', p[1])

def p_callargs(p):
    'callarg : expression COMMA callarg'
    p[0] = ('callarg', p[1], p[3])

def p_callarg(p):
    'callarg : expression'
    p[0] = ('callarg', p[1])


# def p_void(p):
#     'func : FUNC NAME LPAREN arg RPAREN block END'
#     p[0] = ('func', p[2], p[4], p[6])

# def p_function(p):
#     'func : FUNC NAME LPAREN arg RPAREN block END'
#     p[0] = ('func', p[2], p[4], p[6])

# def p_statement_return(p):
#     'return_statement : RETURN expression'
#     p[0] = ('return', p[2])


# def p_args(p):
#     'arg : NAME COMMA arg'
#     p[0] = ('args', p[1], p[3])

# def p_arg(p):
#     'arg : expression'
#     p[0] = ('args', p[1])

def p_instruction(p):
    '''instruction : statement SEMICOLON
    | expression SEMICOLON '''
    p[0] = p[1]


def p_statement_affect(p):
    'statement : NAME AFFECT expression'
    p[0] = ('=', p[1], p[3])


def p_statement_if(p):
    'condition : IF LPAREN boolexpr RPAREN block END'
    p[0] = ('if', p[3], p[5])


def p_statement_if_else(p):
    'condition : IF LPAREN boolexpr RPAREN block ELSE block END'
    p[0] = ('ifelse', p[3], p[5], p[7])


def p_loop_while(p):
    'loop : WHILE LPAREN boolexpr RPAREN block END'
    p[0] = ('while', p[3], p[5])


def p_loop_until(p):
    'loop : UNTIL LPAREN boolexpr RPAREN block END'
    p[0] = ('until', p[3], p[5])


def p_loop_for(p):
    'loop : FOR LPAREN NAME SEMICOLON boolexpr SEMICOLON statement  RPAREN block END'
    p[0] = ('for', p[3], p[5], p[7], p[9])


def p_boolexpr_or(p):
    'boolexpr : boolexpr COR boolexpr'
    p[0] = ('||', p[1], p[3])


def p_boolexpr_and(p):
    'boolexpr : expression CAND expression'
    p[0] = ('&&', p[1], p[3])


def p_boolexpr_comp_gt(p):
    'boolexpr : expression GT expression'
    p[0] = ('>', p[1], p[3])


def p_boolexpr_comp_lt(p):
    'boolexpr : expression LT expression'
    p[0] = ('<', p[1], p[3])


def p_boolexpr_comp_loe(p):
    'boolexpr : expression LOE expression'
    p[0] = ('<=', p[1], p[3])


def p_boolexpr_comp_goe(p):
    'boolexpr : expression GOE expression'
    p[0] = ('>=', p[1], p[3])


def p_boolexpr_comp_equals(p):
    'boolexpr : expression EQUALS expression'
    p[0] = ('==', p[1], p[3])


def p_boolexpr_comp_different(p):
    'boolexpr : expression DIFFERENT expression'
    p[0] = ('!=', p[1], p[3])


def p_expression_print(p):
    'expression : PRINT LPAREN expression RPAREN'
    p[0] = ('PRINT', p[3])


def p_expression_binop_plus(p):
    'expression : expression PLUS expression'
    p[0] = ('+', p[1], p[3])


def p_expression_binop_times(p):
    'expression : expression TIMES expression'
    p[0] = ('*', p[1], p[3])


def p_expression_binop_minus(p):
    'expression : expression MINUS expression'
    p[0] = ('-', p[1], p[3])


def p_expression_binop_divide(p):
    'expression : expression DIVIDE expression'
    p[0] = ('/', p[1], p[3])


def p_expression_binop_or(p):
    'expression : expression OR expression'
    p[0] = ('|', p[1], p[3])


def p_expression_binop_and(p):
    'expression : expression AND expression'
    p[0] = ('&', p[1], p[3])

# def p_expression_func_call(p):
#     'expression : NAME LPAREN argcall RPAREN'
#     p[0] = ('func_call', p[1], p[3])

# def p_arg_call(p):
#     'argcall : expression COMMA argcall'
#     p[0] = ('argCall', p[1], p[3])

# def p_arg_calls(p):
#     'argcall : expression'
#     p[0] = ('argcall', p[1], p[3])


def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]


def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]


def p_expression_name(p):
    'expression : NAME'
    p[0] = ('var', p[1])


def p_error(p):
    print("Syntax error at '%s'" % p.value)


yacc.yacc()


def evalInst(t):
    #print('evalInst de ', t)
    if type(t) is tuple:
        if t[0] == '=':
            exists = False
            for scope in stack:
                if t[1] in scope:
                    exists = True
            if t[1] not in reserved and not exists:
                stack[len(stack) - 1][t[1]] = evalExpr(t[2])

               
        if t[0] == 'expression':
            print('CALC> ', evalInst(t))

        if t[0] == 'block':
            for i in range(1, len(t)):
                evalInst(t[i])

        if t[0] == 'funcdef':
            functions[t[1]] = (evalInst(t[2]), t[3], t[4])


        if t[0] == 'voidcall':
            var = {}
            args = evalInst(t[2])
            if (args != None and  functions[t[1]][0] == None) or (args == None and  functions[t[1]][0] != None) or (not len(args) == len(functions[t[1]][0])):
                raise ValueError("Mismatching number of args !")
            for i, argName in enumerate(functions[t[1]][0]):
                var[argName] = args[i]
            stack.append(var) 
            evalInst(functions[t[1]][1])
            stack.pop()



        # if t[0] == 'func':
        #     functions[t[1]] = ('funccall',evalInst(t[2]), t[3])

        # if t[0] == 'funccall':

        if t[0] == 'declarg':
            args = [t[1],]
            if len(t) == 3:
                args = args + (evalInst(t[2]))

            return args

        if t[0] == 'callarg':
            args = [evalExpr(t[1]),]
            if len(t) == 3:
                args = args + evalInst(t[2])
            return args

        if t[0] == 'PRINT':
            print(evalExpr(t[1]))

        if t[0] == 'if':
            if evalBool(t[1]):
                evalInst(t[2])

        if t[0] == 'ifelse':
            if evalBool(t[1]):
                evalInst(t[2])
            else:
                evalInst(t[3])

        if t[0] == 'while':
            while evalBool(t[1]):
                evalInst(t[2])

        if t[0] == 'until':
            while not evalBool(t[1]):
                evalInst(t[2])

        if t[0] == 'for':
            stack.append({t[1] : 0})
            while evalBool(t[2]):
                evalInst(t[4])
                evalInst(t[3])
            stack.pop()


def evalBool(t):
    #print('evalBool de ', t)
    if type(t) is bool:
        return t
    if type(t) is tuple:
        if t[0] == '||':
            return evalBool(t[1]) or evalBool(t[2])
        if t[0] == '&&':
            return evalBool(t[1]) and evalBool(t[2])
        if t[0] == '>':
            return evalExpr(t[1]) > evalExpr(t[2])
        if t[0] == '<':
            return evalExpr(t[1]) < evalExpr(t[2])
        if t[0] == '<=':
            return evalExpr(t[1]) <= evalExpr(t[2])
        if t[0] == '>=':
            return evalExpr(t[1]) >= evalExpr(t[2])
        if t[0] == '==':
            return evalExpr(t[1]) == evalExpr(t[2])
        if t[0] == '!=':
            return evalExpr(t[1]) != evalExpr(t[2])
    return "UNK"


def evalExpr(t):
    #print('evalExpr de ', t)
    if type(t) is int:
        return t
    if type(t) is tuple:
        if t[0] == '+':
            return evalExpr(t[1]) + evalExpr(t[2])
        if t[0] == '*':
            return evalExpr(t[1]) * evalExpr(t[2])
        if t[0] == '/':
            return evalExpr(t[1]) / evalExpr(t[2])
        if t[0] == '-':
            return evalExpr(t[1]) - evalExpr(t[2])
        if t[0] == '|':
            return evalExpr(t[1]) | evalExpr(t[2])
        if t[0] == '&':
            return evalExpr(t[1]) & evalExpr(t[2])
        if t[0] == 'var':
            for scope in reversed(stack):
                if t[1] in scope:
                    return scope[t[1]]
            raise ValueError('Unknown variable :', t[1]) 
        if t[0] == 'funccall':
            var = {}
            args = evalInst(t[2])
            if (args != None and  functions[t[1]][0] == None) or (args == None and  functions[t[1]][0] != None) or (not len(args) == len(functions[t[1]][0])):
                raise ValueError("Mismatching number of args !")
            for i, argName in enumerate(functions[t[1]][0]):
                var[argName] = args[i]
            stack.append(var)
            evalInst(functions[t[1]][1])
            res =  evalExpr(functions[t[1]][2])
            stack.pop()
            return res



    return 'UNK'


# operate from a string
# s = '''old_number = 0;
# number = 1;
# while(old_number < 145)
# out(old_number);
# new_number = number + old_number;
# old_number = number;
# number = new_number;
# end'''
# yacc.parse(s)


if len(sys.argv) > 1:
    data = open(sys.argv[1], 'r')
    yacc.parse(data.read())
else:
    while True:
        s = input('/>')
        yacc.parse(s)