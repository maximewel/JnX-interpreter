''' 
    Ce module permet la compilation de fichier JNX qui donne,
    après compilation, un nouveau fichier de type XML

    JNX-Interpreter
    He-arc 2020, INF-DLMb
    Maxime Welcklen & Steve Mendes Reis
'''

import ast
from ast import addToClass
from functools import reduce
from parserast import parse
import sys
import os

# pylint: disable=function-redefined

''' --- init variables --- '''
vars = {} # track variables
currentVar = None
countLines = 0 # it allows to keep track tabulation, to correctly format output

''' --- Nodes gestion --- '''

def interpretList(elements):
    ''' Util function to interpret all childrens and merge them
        into one string'''
    return reduce(lambda a,b: a+b, [c.interpret() for c in elements])

def interpretChildren(node: ast.Node):
    ''' Convenient function for node class,
        see InterpretList for more details '''
    return interpretList(node.children)

def error_message(message):
    print(f"Compilation error : {message}")
    exit()

def warning_message(message):
    print(f"Compilation warning : {message}")

@addToClass(ast.DocumentNode)
def interpret(self):
    print("Analysing document...")
    return interpretChildren(self)

@addToClass(ast.BlocNode)
def interpret(self):
    ''' Bloc node is excepted to output something like <tag>content</tag> '''
    global countLines # is used to track tabulation for formatting
    output = "\t"*countLines + f"<{self.tag}"
    if self.info:
        output += self.info.interpret() # we interpret all tags' attributes
    output += ">\n"
    countLines += 1
    output += interpretChildren(self)
    countLines -= 1
    output += "\t"*countLines + f"</{self.tag}>\n"

    return output

@addToClass(ast.TokenNode)
def interpret(self):
    global countLines
    return "\t"*countLines + self.tok + "\n"

@addToClass(ast.InlineNode)
def interpret(self):
    ''' Simple autoclose tags <tag attribs />'''
    global countLines
    output = "\t"*countLines + f"<{self.tag}"
    if self.info:
        output += self.info.interpret()
    output += "/>\n"

    return output

@addToClass(ast.CommentNode)
def interpret(self):
    ''' Comment section produce <!-- COMMENT -->'''
    global countLines
    return "\t"*countLines + f"<!-- {self.comment} -->\n"

@addToClass(ast.InfoNode)
def interpret(self):
    ''' Used as a container for attribute nodes '''
    return interpretChildren(self)

@addToClass(ast.AttributeNode)
def interpret(self):
    ''' Attribue node is a pair key,value '''
    return f" {self.children[0].tok}={self.children[1].tok}"

"""  ---- JINX-NODES ----   """
@addToClass(ast.JnxGetNode)
def interpret(self):
    ''' GetNode is used to retrieve a var by its name'''
    name = self.name
    output = ""
    try: 
        output = "\t"*countLines + str(vars[name]) + "\n"
    except:
        error_message(f"variable '{name}' does not exist !")
        
    return output

@addToClass(ast.JnxVarNode)
def interpret(self):
    ''' VarNode are variables, it could represent a single value
        or a list of values. It should have jnx:value inside of it.
    '''
    global currentVar
    name = self.name

    if self.name in vars:
        warning_message(f"var '{self.name}' already set, this may cause unwanted behaviors, you should considering changing variable's name")

    vars[name] = [] # we create a new variable in our dictionnary
    currentVar = name # we set the current var, so the jnx:value can retrieve it.
    output = ""

    output += interpretChildren(self)

    currentVar = None

    return output

@addToClass(ast.JnxValueNode)
def interpret(self):
    ''' JnxValue is a value to put on a var node '''
    global currentVar
    if not currentVar:
        error_message(f"value '{self.value}' is not surrounded by a variable")
    vars[currentVar].append(self.value)
    return ""

@addToClass(ast.JnxForeachNode)
def interpret(self):
    ''' 
        JnxForeachNode allows to do a foreach iteration
        on a Var node with one or more values
    '''
    output = ""

    if self.itName in vars:
        warning_message(f"var '{self.itName}' already set, this may cause unwanted behaviors, you should considering changing variable's name")
    
    if self.collecName not in vars:
        error_message(f"Foreach is trying to reach '{self.collecName}' variable but it does not exist !")

    for it in vars[self.collecName]:
        vars[self.itName] = it
        output += interpretChildren(self)

    del vars[self.itName] # cleaning as var is no more in the scope

    return output

@addToClass(ast.JnxForNode)
def interpret(self):
    ''' 
        JnxForNode allows to do a for range based
        the current variable i is setted for every iteration
    '''
    output = ""

    if self.itName in vars:
        warning_message(f"var '{self.itName}' already set, this may cause unwanted behaviors, you should considering changing variable's name")

    for it in range(self.start, self.to, self.step):
        vars[self.itName] = it
        output += interpretChildren(self)
    
    del vars[self.itName] # cleaning as var is no more in the scope

    return output

@addToClass(ast.JnxHeader)
def interpret(self):
    ''' Represent a header in a xml document, nothing special '''
    return f"<?xml{interpretChildren(self)} ?>\n\n"

if __name__ == "__main__":
    prog = open(sys.argv[1]).read()
    result = parse(prog)
    compiled = result.interpret()

    fileWithoutPath = sys.argv[1].split('\\')[-1]
    fileWithoutExtension = os.path.splitext(fileWithoutPath)[0]
    name = os.getcwd() + "\\output\\XML\\" + fileWithoutExtension + ".xml"
    outfile = open(name,'w')
    outfile.write(compiled)
    outfile.close()

    print("Wrote output to",name)
