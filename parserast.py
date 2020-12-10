import ply.lex as lex
import ply.yacc as yacc
import sys
import os

from lex import tokens
import ast

jnxNodes = {
    'get' : ast.JnxGetNode(),
    'var' : ast.JnxVarNode(),
    'foreach' : ast.JnxForeachNode(),
    'value' : ast.JnxValueNode(),
    'for' : ast.JnxForNode(),
}

precedence = (
    ('left', 'TRANSFORM_NODE'),
)

# ---- BLOC AND LINES ----

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
    ''' line : balise_start token_sequence balise_end
    | balise_start bloc balise_end 
    | balise_autoclose
    | comment '''
    try :
        p[0] = ast.LineNode([p[1], p[2], p[3]])
    except IndexError:
        p[0] = p[1]
    
# ---- BALISES ----

def p_autoBalise(p):
    ''' balise_autoclose : tag "/" ">"
    | tag attributes "/" ">" '''
    if len(p) > 4:
        p[0] = ast.LineNode([ast.BaliseStartNode([p[1], p[2]]), ast.TokenNode('VIDE'), ast.BaliseEndNode(p[1])])
    else:
        p[0] = ast.LineNode([ast.BaliseStartNode(p[1]), ast.TokenNode('VIDE'), ast.BaliseEndNode(p[1])])

def p_balise_start(p):
    ''' balise_start : tag ">"
    | tag attributes ">"'''
    if len(p) > 3:
        p[0] = ast.BaliseStartNode([p[1], p[2]])
    else :
        p[0] = ast.BaliseStartNode(p[1])


# TAGS : XML, JNX, JNX-Header
def p_tag(p):
    ''' tag : "<" token '''
    p[0] = p[2]

def p_tag_jinx(p):
    ''' tag : JNX_TAG_START '''
    jinxWord = p[1].split(":")[-1]
    try:
        p[0] = jnxNodes[jinxWord]
    except KeyError :
        error_message(p[1], f"{jinxWord} is not a know jinx word !")

def p_tag_jinx_header(p):
    ''' tag : JNX_TAG_HEADER '''
    p[0] = ast.JnxHeader()


def p_balise_end(p):
    ''' balise_end : "<" "/" token  ">" '''
    p[0] = ast.BaliseEndNode(p[3])

def p_balise_end_jinx(p):
    ''' balise_end : "<" JNX_TAG_END '''
    jinxWord = p[2].split(":")[-1].replace(">", "")
    try:
        p[0] =  ast.BaliseEndNode(jnxNodes[jinxWord])
    except KeyError :
        error_message(p[1], f"{jinxWord} is not a know jinx word !")

def p_comment(p):
    ''' comment : COMMENT '''
    p[0] = ast.CommentNode(p[1].replace("<!--", "").replace("-->", ""))
# ---- ATTRIBUTES ---- 

def p_attributes_sequence(p):
    ''' attributes : attribute 
    | attributes attribute'''
    try:
        p[0] = ast.InfoNode(p[1].children + [p[2]])
    except :
        p[0] = ast.InfoNode(p[1])

def p_attribute(p):
    ''' attribute : token "=" ATTRIB_VAL '''
    p[0] = ast.AttributeNode([p[1], ast.TokenNode(p[3])])

# ---- TOKENS AND STRINGS ---- 

def p_token(p):
    ''' token : IDENTIFIER '''
    p[0] = ast.TokenNode(p[1])

def p_token_sequence(p):
    ''' token_sequence : token
    | token_sequence token '''
    try:
        p[0] = ast.TokenNode(p[1].tok + " " + p[2].tok)
    except :
        p[0] = p[1]

# --- Error special case --- 

def error_message(p, message):
    print(f"Error message : {message}")
    p_error(p)

def p_error(p) :
    print("syntax error in line {}".format(p.lineno))
    parser.errok()

parser = yacc.yacc(outputdir = "generated")

if __name__ == "__main__":
    #build the graph
    filename = os.getcwd() + "\\" + sys.argv[1]
    with open(filename) as prog :
        result = yacc.parse(prog.read(), debug=True)
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