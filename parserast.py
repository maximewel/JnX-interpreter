''' 
    Ce module permet de parser les fichiers de type JNX

    Il permet aussi de frabriquer ("coudre") un arbre pour avoir
    une représentation de notre arbre syntaxique

    JNX-Interpreter
    He-arc 2020, INF-DLMb
    Maxime Welcklen & Steve Mendes Reis
'''

import ply.lex as lex
import ply.yacc as yacc
import sys
import os

from lex import tokens
import ast

def getValFromAttributeName(nodes, name, default=None):
    '''
        Helper function to retrieve attribute's value based on a name
        If the attribute does not exist it will return 'default' parameter 
    '''
    attrib = getAttributeFromAttributeName(nodes, name)

    if attrib is None:
        return default

    return attrib.children[1].tok[1:-1] # get ride of quotes

def getAttributeFromAttributeName(nodes, name):
    ''' Helper function to retrieve attribute based on a name '''
    for child in nodes.children:
        if type(child) is ast.AttributeNode:
            if child.children[0].tok == name:
                return child
    return None # replace by an error ?

def JnxForeach(p):
    attribs = p[1][1]
    collectionName = getValFromAttributeName(attribs, "in")
    itName = getValFromAttributeName(attribs, "name", "it")

    if collectionName is None:
        error_message(p,"jnx:for is missing collection parameter !")

    return ast.JnxForeachNode(p[2], itName, collectionName)

def JnxFor(p):
    attribs = p[1][1]
    start = getValFromAttributeName(attribs, "from")
    to = getValFromAttributeName(attribs, "to")
    step = int(getValFromAttributeName(attribs, "step", "1"))
    itName = getValFromAttributeName(attribs, "name", "it")

    if start is None or to is None:
        error_message(p,"jnx:for is missing either 'from' or 'to' parameter !")

    start = int(start); to = int(to) #convert to int as we receive str parameter

    # semantic verification 
    sem = ((to - start)/step)
    if sem < 0:
        error_message(p, f"For loop with values start={start}, to={to} and step={step} may endup in an infinite loop !")

    return ast.JnxForNode(p[2], start, to, step, itName)

def JnxGet(p):
    attribs = p[2]
    name = getValFromAttributeName(attribs, "name")

    if name is None:
        error_message(p,"jnx:get is missing 'name' parameter !")

    return ast.JnxGetNode(name)

def JnxVar(p):
    attribs = p[1][1]
    name = getValFromAttributeName(attribs, "name")

    if name is None:
        error_message(p,"jnx:var is missing 'name' parameter !")

    node = ast.JnxVarNode(p[2], name)

    return node

def JnxValue(p):
    value = p[2].tok

    return ast.JnxValueNode(value)

jnxNodes = {
    'get' : JnxGet,
    'var' : JnxVar,
    'foreach' : JnxForeach,
    'value' : JnxValue,
    'for' : JnxFor,
}

precedence = (
    ('left', 'TRANSFORM_NODE'),
)

# ---- BLOC AND LINES ----
def p_document(p):
    ''' document : jinx_header bloc 
    | bloc'''
    try:
        p[0] = ast.DocumentNode([p[1]] + p[2])
    except:
        p[0] = p[1]

def p_bloc(p):
    ''' bloc : line %prec TRANSFORM_NODE 
    | inline %prec TRANSFORM_NODE 
    | line_jnx %prec TRANSFORM_NODE
    | comment '''
    p[0] = [p[1]] # Starting a nodes' list

def p_bloc_multiple(p):
    ''' bloc : bloc line
    | bloc inline 
    | bloc line_jnx '''
    p[1].append(p[2]) # a bloc is a nodes' list, so here we basically add a new node to the list
    p[0] = p[1]

def p_line(p):
    ''' line : balise_start token_sequence balise_end
    | balise_start bloc balise_end '''
    if p[1][0].tok != p[3][0].tok: # ensure that start and end tag match 
        error_message(p, f"Start and end tag doesn't match : {p[1][0].tok} != {p[3][0].tok}")

    node = ast.BlocNode(p[2], p[1][0].tok) # we create a bloc for the specified tag

    if len(p[1]) > 1:
        node.info = p[1][1] # we set attributes for the tag

    p[0] = node

def p_line_jnx(p):
    ''' line_jnx : balise_start_jnx token_sequence balise_end_jnx
    | balise_start_jnx bloc balise_end_jnx '''
    
    if p[1][0] != p[3]: # ensure that start and end tag match 
        error_message(p, f"Start and end JNX tag doesn't match : {p[1][0]} != {p[3]}")
    
    jinxWord = p[1][0] # retrieving the jinxword to call the correct object constructor
    
    try:
        p[1] = jnxNodes[jinxWord](p) # creating the node needed
    except IndexError:
        error_message(p, f"{jinxWord} is not a know jinx word !") # if node name doesn't exist we throw an error 

    p[0] = p[1]
    
# ---- BALISES ----
def p_auto_balise(p):
    ''' inline : tag "/" ">"
    | tag attributes "/" ">" '''
    node = ast.InlineNode(p[1].tok) # inline tag so we directly create inline node

    if len(p) > 4:
        node.info = p[2] # add attributs if there is any
    
    p[0] = node

def p_auto_balise_jnx(p):
    ''' line_jnx : tag_jnx "/" ">"
    | tag_jnx attributes "/" ">" '''
    p[0] = jnxNodes[p[1]](p) # autoclose jnx tag, we directly create jnx node

def p_balise_start(p):
    ''' balise_start : tag ">"
    | tag attributes ">"'''
    if len(p) > 3: 
        p[0] = [p[1], p[2]] # if there is attributes
    else :
        p[0] = [p[1]]

def p_balise_start_jnx(p):
    ''' balise_start_jnx : tag_jnx ">"
    | tag_jnx attributes ">"'''
    if len(p) > 3:
        p[0] = [p[1], p[2]] # if there is attributes
    else:
        p[0] = [p[1]]

# TAGS : XML, JNX, JNX-Header
def p_tag(p):
    ''' tag : "<" token '''
    p[0] = p[2]

def p_tag_jinx(p):
    ''' tag_jnx : JNX_TAG_START '''
    jinxWord = p[1].split(":")[-1]
    p[0] = jinxWord

def p_jinx_header(p):
    ''' jinx_header : JNX_TAG_HEADER_START attributes JNX_TAG_HEADER_END'''
    p[0] = ast.JnxHeader(p[2].children)

def p_balise_end(p):
    ''' balise_end : "<" "/" token  ">" '''
    p[0] = [p[3]]

def p_balise_end_jinx(p):
    ''' balise_end_jnx : "<" JNX_TAG_END '''
    jinxWord = p[2].split(":")[-1].replace(">", "")
    p[0] = jinxWord

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