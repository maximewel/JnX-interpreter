import ply.lex as lex
import ply.yacc as yacc
import sys
import os

from lex import tokens
import ast

operations = {
    "+"   : lambda x,y: x+y,
    "-"   : lambda x,y: x-y,
    "*"   : lambda x,y: x*y,
    "/"   : lambda x,y: x/y,
}

precedence = (
    ("left", "ADD_OP"),
    ("left", "MUL_OP"),
    ('right', 'UMINUS'),
)


def p_document(p):
    '''document : LINE document'''

def p_line(p):
    '''line : XML_line
    | JNX_line 
    '''

def p_XML_line(p):
    """XML_line : XML"""
    p[0] = ast.XMLNode(p[1])

def p_JNX_line(p):
    """JNX_line : JNX"""
    p[0] = ast.JNXNode(p[1])

def p_error(p) :
    print("syntax error in line {}".format(p.lineno))
    parser.errok()

parser = yacc.yacc(outputdir = "generated")

if __name__ == "__main__":
    filename = os.getcwd() + "\\" + sys.argv[1]
    with open(filename) as prog :
        result = yacc.parse(prog.read())
        print(result)
    graph = result.makegraphicaltree()
    name = os.path.splitext(sys.argv[1])[0] + "-ast.pdf"
    graph.write_pdf(name)
    print("file generated : {}".format(name))

def parse(program):
    result = yacc.parse(program)
    return result