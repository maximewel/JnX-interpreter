import ply.lex as lex
import ply.yacc as yacc
import sys
import os

from lex import tokens
import ast

"""operations = {
    "+"   : lambda x,y: x+y,
    "-"   : lambda x,y: x-y,
    "*"   : lambda x,y: x*y,
    "/"   : lambda x,y: x/y,
}

precedence = (
    ("left", "ADD_OP"),
    ("left", "MUL_OP"),
    ('right', 'UMINUS'),
)"""


def p_document(p):
    ''' document : line 
    | line document '''
    p[0] = ast.DocumentNode(p[1])

def p_line(p):
    ''' line : balise_start content balise_end '''
    p[0] = ast.LineNode([p[1], p[2], p[3]])

def p_autoBalise(p):
    ''' balise_start : "<" content "/" ">" '''
    p[0] = ast.BaliseStartNode(p[2])

def p_balise_start(p):
    ''' balise_start : "<" content ">" '''
    p[0] = ast.BaliseStartNode(p[2])

def p_balise_end(p):
    ''' balise_end : "<" "/" content  ">" '''
    p[0] = ast.BaliseEndNode(p[3])

def p_content(p):
    ''' content : IDENTIFIER
    | line'''
    p[0] = ast.ContentNode(p[1])

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