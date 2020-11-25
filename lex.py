import ply.lex as lex
import sys
import os

tokens = (
    'IDENTIFIER',
    'JNX_TAG',
    'ATTRIB_VAL',
)

#reserved words
literals = r'[</>="]'
reserved_words = (
    #"jnx",
)
tokens += tuple([reserved.upper() for reserved in reserved_words]) #add reserved words to the list of tokens, upper case

def t_JNX_TAG(t):
    r"<jnx:\w*\b"
    return t

#The identifier is not inline anymore : A bit more complex, needs to be factorised in a function
def t_IDENTIFIER(t):
    r"[A-Za-z_][\w]*"
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