import ast
from ast import addToClass
from functools import reduce
from parserast import parse
import sys
import os

# pylint: disable=function-redefined

""" --- init variables --- """
vars = {}
tags = []
lastVar = None
countLines = 0

""" --- Nodes gestion ---"""

"""         ---- XML-Structure-Nodes ----
DocumentNode
BlocNode
""" """     ---- LINES-Nodes ----
LineNode
InlineNode
AttributeNode
CommentNode
""" """     ---- JINX-NODES ----
JnxGetNode
JnxVarNode
JnxForeachNode
JnxValueNode
JnxForNode
JnxHeader
"""

def interpretList(elements):
    return reduce(lambda a,b: a+b, [c.interpret() for c in elements])

def interpretChildren(node):
    return interpretList(node.children)

@addToClass(ast.DocumentNode)
def interpret(self):
    print("Analysing document...")
    return interpretChildren(self)

@addToClass(ast.LineNode)
def interpret(self):
    global countLines
    output = "\t"*countLines + f"<{self.tag}"
    if self.info:
        output += self.info.interpret()
    output += ">\n"
    countLines += 1
    output += "\t"*0 + interpretChildren(self)
    countLines -= 1
    output += "\t"*countLines + f"</{self.tag}>\n"

    return output

@addToClass(ast.TokenNode)
def interpret(self):
    global countLines
    return "\t"*countLines + self.tok + "\n"

@addToClass(ast.InlineNode)
def interpret(self):
    global countLines
    output = "\t"*countLines + f"<{self.tag}"
    if self.info:
        output += self.info.interpret()
    output += "/>\n"

    return output

@addToClass(ast.BlocNode)
def interpret(self):
    return interpretChildren(self)

@addToClass(ast.CommentNode)
def interpret(self):
    global countLines
    return "\t"*countLines + f"<!-- {self.comment} -->\n"

""" ---- LINES-Nodes ---- """

@addToClass(ast.InfoNode)
def interpret(self):
    return interpretChildren(self)

@addToClass(ast.AttributeNode)
def interpret(self):
    return f" {self.children[0].tok}={self.children[1].tok}"

"""  ---- JINX-NODES ----   """
def getValFromAttributeName(node, name, default=None):
    attrib = getAttributeFromAttributeName(node, name)

    if attrib is None:
        return default

    return attrib.children[1].tok[1:-1] # get ride of quotes

def getAttributeFromAttributeName(node, name):
    for child in node.children:
        if type(child) is ast.AttributeNode:
            if child.children[0].tok == name:
                return child
    return None # replace by an error ?

@addToClass(ast.JnxGetNode)
def interpret(self):
    value = getValFromAttributeName(self, "name")
    return "\t"*countLines + str(vars[value]) + "\n"

@addToClass(ast.JnxVarNode)
def interpret(self):
    name = getValFromAttributeName(self, "name")
    collec = []

    if type(self.children[-1]) is ast.BlocNode and len(self.children[-1].children):
        for c in self.children[-1].children:
            val = c.interpret()
            collec.append(val)

        vars[name] = collec

    return ""


@addToClass(ast.JnxValueNode)
def interpret(self):
    return self.children[0].tok

@addToClass(ast.JnxForeachNode)
def interpret(self):
    output = ""
    collectionName = getValFromAttributeName(self, "in")
    itName = getValFromAttributeName(self, "name")

    for it in vars[collectionName]:
        vars[itName] = it
        output += self.children[-1].interpret()

    return output

@addToClass(ast.JnxForNode)
def interpret(self):
    output = ""
    start = int(getValFromAttributeName(self, "from"))
    to = int(getValFromAttributeName(self, "to"))
    step = int(getValFromAttributeName(self, "step", "1"))
    itName = getValFromAttributeName(self, "name", "it")

    for it in range(start, to, step):
        vars[itName] = it
        output += self.children[-1].interpret()

    return output

@addToClass(ast.JnxHeader)
def interpret(self):
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
