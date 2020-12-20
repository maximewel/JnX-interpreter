import ply.lex as lex
import ply.yacc as yacc
import sys
import os

from lex import tokens
import ast

jnxNodes = {
    'get' : lambda: ast.JnxGetNode(),
    'var' : lambda: ast.JnxVarNode(),
    'foreach' : lambda: ast.JnxForeachNode(),
    'value' : lambda: ast.JnxValueNode(),
    'for' : lambda: ast.JnxForNode(),
}

precedence = (
    ('left', 'TRANSFORM_NODE'),
)

# ---- BLOC AND LINES ----
def p_document(p):
    ''' document : jinx_header bloc 
    | bloc'''
    try:
        p[0] = ast.BlocNode([p[1]] + p[2].children)
    except:
        p[0] = p[1]

def p_bloc(p):
    ''' bloc : line %prec TRANSFORM_NODE 
    | inline %prec TRANSFORM_NODE 
    | line_jnx %prec TRANSFORM_NODE
    | comment '''
    p[0] = ast.BlocNode(p[1])

def p_bloc_multiple(p):
    ''' bloc : bloc line
    | bloc inline 
    | bloc line_jnx '''
    p[0] = ast.BlocNode(p[1].children + [p[2]])

def p_line(p):
    ''' line : balise_start token_sequence balise_end
    | balise_start bloc balise_end '''
    try :
        if p[1][0].tok != p[3][0].tok:
            error_message(p, f"Start and end tag doesn't match : {p[1][0].tok} != {p[3][0].tok}")
        
        node = ast.LineNode(p[2], p[1][0].tok)
        if len(p[1]) > 1:
            node.info = p[1][1]

        p[0] = node
    except IndexError:
        p[0] = p[1]

def p_line_jnx(p):
    ''' line_jnx : balise_start_jnx token_sequence balise_end_jnx
    | balise_start_jnx bloc balise_end_jnx '''
    try :
        if type(p[1]) != type(p[3]):
            error_message(p, "Start and end JNX tag doesn't match !")
        p[1].children.append(p[2])
        p[0] = p[1]
    except IndexError:
        p[0] = p[1]

def p_line_autoclose_jnx(p):
    ''' line_jnx : balise_autoclose_jnx '''
    p[0] = p[1]

def p_inline(p):
    ''' inline : balise_autoclose '''
    tag = p[1].pop(0).tok
    node = ast.InlineNode(tag)
    if len(p[1]) > 0:
        node.info = p[1][0]

    p[0] = node
# ---- BALISES ----

def p_auto_balise(p):
    ''' balise_autoclose : tag "/" ">"
    | tag attributes "/" ">" '''
    if len(p) > 4:
        p[0] = [p[1], p[2]]
    else:
        p[0] = [p[1]]

def p_auto_balise_jnx(p):
    ''' balise_autoclose_jnx : tag_jnx "/" ">"
    | tag_jnx attributes "/" ">" '''
    if len(p) > 4:
        [p[1].children.append(c) for c in p[2].children]

    p[0] = p[1]

def p_balise_start(p):
    ''' balise_start : tag ">"
    | tag attributes ">"'''
    if len(p) > 3:
        p[0] = [p[1], p[2]]
    else :
        p[0] = [p[1]]

def p_balise_start_jnx(p):
    ''' balise_start_jnx : tag_jnx ">"
    | tag_jnx attributes ">"'''
    if len(p) > 3:
        [p[1].children.append(c) for c in p[2].children]

    p[0] = p[1]

# TAGS : XML, JNX, JNX-Header
def p_tag(p):
    ''' tag : "<" token '''
    p[0] = p[2]

def p_tag_jinx(p):
    ''' tag_jnx : JNX_TAG_START '''
    jinxWord = p[1].split(":")[-1]
    try:
        p[0] = jnxNodes[jinxWord]()
    except KeyError :
        error_message(p[1], f"{jinxWord} is not a know jinx word !")

def p_jinx_header(p):
    ''' jinx_header : JNX_TAG_HEADER_START attributes JNX_TAG_HEADER_END'''
    p[0] = ast.JnxHeader(p[2].children)

def p_balise_end(p):
    ''' balise_end : "<" "/" token  ">" '''
    p[0] = [p[3]]

def p_balise_end_jinx(p):
    ''' balise_end_jnx : "<" JNX_TAG_END '''
    jinxWord = p[2].split(":")[-1].replace(">", "")
    try:
        p[0] = jnxNodes[jinxWord]()
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
        result = yacc.parse(prog.read(), debug=False)
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