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
"""
precedence = (
    ('left', 'TRANSFORM_NODE'),
)

def p_document(p):
    ''' document : bloc '''
    p[0] = p[1]

def p_bloc(p):
    ''' bloc : line %prec TRANSFORM_NODE '''
    p[0] = ast.BlocNode(p[1])

def p_bloc_multiple(p):
    ''' bloc : bloc line '''
    p[0] = ast.BlocNode(p[1].children + [p[2]])

def p_line(p):
    ''' line : balise_start content balise_end
    | balise_start bloc balise_end 
    | balise_autoclose'''
    try :
        p[0] = ast.LineNode([p[1], p[2], p[3]])
    except IndexError:
        p[0] = p[1]

def p_autoBalise(p):
    ''' balise_autoclose : "<" token "/" ">" '''
    p[0] = ast.LineNode([p[2], ast.TokenNode("VIDE"), p[2]])

def p_balise_start(p):
    ''' balise_start : "<" content ">" '''
    p[0] = ast.BaliseStartNode(p[2])

def p_balise_end(p):
    ''' balise_end : "<" "/" content  ">" '''
    p[0] = ast.BaliseEndNode(p[3])

def p_content(p):
    ''' content : token
    | token content'''
    p[0] = p[1]

def p_attribute(p):
    ''' assignement : IDENTIFIER "=" ATTRIB_VAL '''
    p[0] = ast.AssignNode([ast.TokenNode(p[1]), p[3]])

def p_token(p):
    ''' token : IDENTIFIER '''
    p[0] = ast.TokenNode(p[1])

def p_error(p) :
    print("syntax error in line {}".format(p.lineno))
    parser.errok()

parser = yacc.yacc(outputdir = "generated")

if __name__ == "__main__":
    #build the graph
    filename = os.getcwd() + "\\" + sys.argv[1]
    with open(filename) as prog :
        result = yacc.parse(prog.read())
        print(result)
    #write graph to file-ast.pdf in output directory
    graph = result.makegraphicaltree()
    fileWithoutPath = sys.argv[1].split('\\')[-1]
    fileWithoutExtension = os.path.splitext(fileWithoutPath)[0]
    filenameOutput = os.getcwd() + "\\output\\graphes\\" + fileWithoutExtension + "-ast.pdf"
    graph.write_pdf(filenameOutput)

def parse(program):
    result = yacc.parse(program)
    return result