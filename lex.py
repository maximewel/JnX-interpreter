''' 
    Ce module concerne la partie lexicale de l'interpreteur

    JNX-Interpreter
    He-arc 2020, INF-DLMb
    Maxime Welcklen & Steve Mendes Reis
'''

import ply.lex as lex
import sys
import os

tokens = (
    'IDENTIFIER',
    'JNX_TAG_HEADER_START',
    'JNX_TAG_HEADER_END',
    'JNX_TAG_START',
    'JNX_TAG_END',
    'ATTRIB_VAL',
    'COMMENT',
)

#reserved words
literals = r'[</>="]'
reserved_words = (
)
tokens += tuple([reserved.upper() for reserved in reserved_words]) #add reserved words to the list of tokens, upper case

''' --- JNX attributes --- '''

#JNX start/end tokens
def t_JNX_TAG_START(t):
    r"<jnx:\w*(\b)?"
    return t

def t_JNX_TAG_END(t):
    r"/jnx:\w*>"
    return t

def t_JNX_TAG_HEADER_START(t):
    r"<\?jnx"
    return t

def t_JNX_TAG_HEADER_END(t):
    r"\?>"
    return t

def t_COMMENT(t):
    r"<!--.*?-->"
    return t

#attributes values ("...")
def t_ATTRIB_VAL(t):
    r"\".*?\""
    return t

''' --- From compiler course --- '''
def t_IDENTIFIER(t):
    r"[\w_-]+"
    if t.value in reserved_words:
        t.type = t.value.upper()
    return t

#keep trace of the line
def t_newline(t) :
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t) :
    print("illegal char {}".format(t.value))
    t.lexer.skip(1)

lex.lex()

if __name__ == "__main__":
    filename = os.getcwd() + "\\" + sys.argv[1]
    with open(filename) as prog :
        lex.input(prog.read())
        while 1: 
            tok = lex.token()
            if not tok : 
                break 
            print (" line {}: {}({})".format(tok.lineno, tok.type, tok.value))