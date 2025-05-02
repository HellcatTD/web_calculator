#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
# reference from
# https://github.com/BaseMax/MiniCalculatorInterpreter
import math
import ply.lex as lex
import ply.yacc as yacc

tokens = (
    'NAME',
    'NUMBER_INT', 'NUMBER_DOUBLE',
    'PLUS','MINUS','TIMES','DIVIDE','POW','MOD',
    'EQUALS','COLON',
    'LPAREN','RPAREN',
)
t_NAME    = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_COLON   = r','
t_EQUALS  = r'='
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_POW     = r'\^'
t_MOD     = r'%'
t_ignore = ' \t'



def t_NUMBER_DOUBLE(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print('Integer value too large %d', t.value)
        t.value = 0
    return t

def t_NUMBER_INT(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print('Integer value too large %d', t.value)
        t.value = 0
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')
    
def t_error(t):
    print('Illegal character \'%s\'' % t.value[0])
    t.lexer.skip(1)

precedence = (
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE','MOD'),
    ('left','POW'),
    ('right','UMINUS'),
)

variables = {
    'pi': math.pi,
    'e': math.e,
}
start='statement'

def p_statement_assign(t):
    '''
    statement : NAME EQUALS expression
    '''
    variables[t[1]] = t[3]

def p_statement_expression(t):
    '''
    statement : expression
    '''

    if(writefile == True):  #mode 2
        if(t[1]==None):
            print('Ans : invalid input')
            f.writelines('invalid input\n')
            conn.send(("invalid input").encode())
        else:
            print('Ans = ' + str(t[1]))
            f.writelines(str(t[1])+'\n')
            conn.send(str(t[1]).encode())
    else:                   #not mode 2
        if(t[1]==None):
            print('Send to client: invalid input')
            conn.send(("invalid input").encode())
        else:
            print('Send to client: ' + str(t[1]))
            conn.send(str(t[1]).encode())

def p_expression_binop(t):
    '''
    expression : expression PLUS expression
               | expression MINUS expression
               | expression DIVIDE expression
               | expression TIMES expression
               | expression POW expression
               | expression MOD expression
    '''
    if(t[3] == None):   #exception handling
        t[0] = None
    elif t[2] == '+':
        t[0] = t[1] + t[3]
    elif t[2] == '-':
        t[0] = t[1] - t[3]
    elif t[2] == '*':
        t[0] = t[1] * t[3]
    elif t[2] == '/':
        if(t[3]==0):    #exception handling
            t[0] = None
        else:
            t[0] = t[1] / t[3]
    elif t[2] == '^':
        t[0] = math.pow(t[1],t[3])
    elif t[2] == '%':
        t[0] = t[1] % t[3]

def p_expression_uminus(t):
    '''
    expression : MINUS expression %prec UMINUS
    '''
    t[0] = -t[2]

def p_expression_group(t):
    '''
    expression : LPAREN expression RPAREN
    '''
    t[0] = t[2]

def p_expressions(t):
    '''
    expressions : expressions COLON expression
               | expression
               |
    '''
    if len(t) == 0:
        t[0]=None
        return
    t[0] = [t[1]] if len(t) == 2 else t[1] + [t[3]]

def p_expression_function(t):
    '''
    expression : NAME LPAREN expressions RPAREN
    '''
    if t[1] == 'sin':
        if len(t[3]) == 1:
            t[0]=math.sin(float(t[3][0]))
        else:
            print('%s() function need one arguments' % t[1])
        return
    elif t[1] == 'cos':
        if len(t[3]) == 1:
            t[0]=math.cos(float(t[3][0]))
        else:
            print('%s() function need one arguments' % t[1])
        return
    elif t[1] == 'log':
        if len(t[3]) == 1:
            t[0]=math.log(float(t[3][0]))
        else:
            print('%s() function need one arguments' % t[1])
        return
    elif t[1] == 'log10':
        if len(t[3]) == 1:
            t[0]=math.log10(float(t[3][0]))
        else:
            print('%s() function need one arguments' % t[1])
        return
    elif t[1] == 'log2':
        if len(t[3]) == 1:
            t[0]=math.log2(float(t[3][0]))
        else:
            print('%s() function need one arguments' % t[1])
        return
    elif t[1] == 'exp':
        if len(t[3]) == 1:
            t[0]=math.exp(float(t[3][0]))
        else:
            print('%s() function need one arguments' % t[1])
        return




    elif t[1] == 'sqrt':
        if len(t[3]) == 1:
            t[0]=math.sqrt(float(t[3][0]))
        else:
            print('%s() function need one arguments' % t[1])
        return
    elif t[1] == 'acos':
        if len(t[3]) == 1:
            t[0]=math.acos(float(t[3][0]))
        else:
            print('%s() function need one arguments' % t[1])
        return
    elif t[1] == 'atan':
        if len(t[3]) == 1:
            t[0]=math.atan(float(t[3][0]))
        else:
            print('%s() function need one arguments' % t[1])
        return
    elif t[1] == 'radians':
        if len(t[3]) == 1:
            t[0]=math.radians(float(t[3][0]))
        else:
            print('%s() function need one arguments' % t[1])
        return
    elif t[1] == 'sinh':
        if len(t[3]) == 1:
            t[0]=math.sinh(float(t[3][0]))
        else:
            print('%s() function need one arguments' % t[1])
        return
    elif t[1] == 'cosh':
        if len(t[3]) == 1:
            t[0]=math.cosh(float(t[3][0]))
        else:
            print('%s() function need one arguments' % t[1])
        return
    elif t[1] == 'tanh':
        if len(t[3]) == 1:
            t[0]=math.tanh(float(t[3][0]))
        else:
            print('%s() function need one arguments' % t[1])
        return
    elif t[1] == 'asin':
        if len(t[3]) == 1:
            t[0]=math.asin(float(t[3][0]))
        else:
            print('%s() function need one arguments' % t[1])
        return



    elif t[1] == 'ceil':
        if len(t[3]) == 1:
            t[0]=math.ceil(float(t[3][0]))
        else:
            print('%s() function need one arguments' % t[1])
        return
    elif t[1] == 'fabs':
        if len(t[3]) == 1:
            t[0]=math.fabs(float(t[3][0]))
        else:
            print('%s() function need one arguments' % t[1])
        return
    elif t[1] == 'factorial':
        if len(t[3]) == 1:
            t[0]=math.factorial(float(t[3][0]))
        else:
            print('%s() function need one arguments' % t[1])
        return
    elif t[1] == 'floor':
        if len(t[3]) == 1:
            t[0]=math.floor(float(t[3][0]))
        else:
            print('%s() function need one arguments' % t[1])
        return
    elif t[1] == 'copysign':
        if len(t[3]) == 2:
            t[0]=math.copysign(int(t[3][0]), int(t[3][1]))
        else:
            print('%s() function need two arguments' % t[1])
        return
    elif t[1] == 'pow':
        if len(t[3]) == 2:
            t[0]=math.pow(int(t[3][0]), int(t[3][1]))
        else:
            print('%s() function need two arguments' % t[1])
        return
    print('Undefined function \'%s\'' % t[1])
    t[0] = None

def p_expression_number(t):
    '''
    expression : NUMBER_INT
               | NUMBER_DOUBLE
    '''
    t[0] = t[1]

def p_expression_name(t):
    '''
    expression : NAME
    '''
    try:
        t[0] = variables[t[1]]
    except LookupError:
        print('Undefined name \'%s\'' % t[1])
        t[0] = None

def p_error(t):
    print('Syntax error at \'%s\'' % t.value)

# lexer = lex.lex()
lexer = lex.lex(optimize=1)
# parser = yacc.yacc()
parser = yacc.yacc(debug=0, write_tables=0)

HOST = '127.0.0.1'
PORT = 7000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(5)

print('server start at: %s:%s' % (HOST, PORT))
print('wait for connection...')

conn, addr = s.accept()
writefile = False
print('connected by ' + str(addr))

while True:
    indata = conn.recv(1024)
    
    if len(indata) == 0: # connection closed
        conn.close()
        #print('Connection close !')
        break

    if indata.decode() == 'quit mode' :
        print("Quit~\nBack to Mode~")
        continue
    elif indata.decode() == 'write file':
        writefile = True
        


        expected_size = b""
        while len(expected_size) < 8:
            more_size = conn.recv(8 - len(expected_size))
            if not more_size:
                raise Exception("Short file length received")
            expected_size += more_size

        # Convert to int, the expected file length
        expected_size = int.from_bytes(expected_size, 'big')

        # Until we've received the expected amount of data, keep receiving
        packet = b""  # Use bytes, not str, to accumulate
        while len(packet) < expected_size:
            buffer = conn.recv(expected_size - len(packet))
            if not buffer:
                raise Exception("Incomplete file received")
            packet += buffer
        with open('recieved Testcase.txt', 'wb') as f:
            f.write(packet)


        f=open('Ans.txt', mode='w')
        continue
    elif indata.decode() == 'exit write file':
        f.close()
        writefile = False
        continue
    print('recv: ' + indata.decode())
    
    parser.parse(indata.decode())
    
print("Quit~\nConnection close !")