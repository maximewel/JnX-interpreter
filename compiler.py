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
lastVar = None;

""" --- Nodes gestion ---"""

"""         ---- XML-Structure-Nodes ----
DocumentNode
LineNode
BlocNode
""" """     ---- LINES-Nodes ----
InfoNode
TokenNode
AttributeNode
BaliseStartNode
BaliseEndNode
""" """     ---- JINX-NODES ----
JnxGetNode
JnxVarNode
JnxForeachNode
JnxValueNode
JnxForNode
"""

def interpretChildren(node):
    return reduce(lambda a,b: a+b, [c.interpret() for c in node.children])

@addToClass(ast.DocumentNode)
def interpret(self):
    print("Analysing document...")
    return interpretChildren(self)

@addToClass(ast.LineNode)
def interpret(self):
    return interpretChildren(self)

@addToClass(ast.BlocNode)
def interpret(self):
    return interpretChildren(self)

""" ---- LINES-Nodes ---- """

@addToClass(ast.InfoNode)
def interpret(self):
    return interpretChildren(self)

@addToClass(ast.TokenNode)
def interpret(self):
    return self.children[0]

@addToClass(ast.AttributeNode)
def interpret(self):
    return f" {self.children[0]}={self.children[1]}"

@addToClass(ast.BaliseStartNode)
def interpret(self):
    currentTag = self.children[0]
    tags.append(currentTag)
    output = f"{currentTag}"
    if len(self.children) >= 2:
        output += f" {self.children[0].interpret()}"
    
    return output

@addToClass(ast.BaliseEndNode)
def interpret(self):
    lastTag = tags.pop(0)
    if (lastTag != self.children[0]):
        pass # output error and exit

    return f"{lastTag}"

"""  ---- JINX-NODES ----   """
def getValFromAttributeName(node, name):
    attrib = getAttributeFromAttributeName(node, name)

    if attrib is None:
        pass #error

    return attrib.children[1]

def getAttributeFromAttributeName(node, name):
    for child in node.children:
        if not isinstance(child, ast.AttributeNode):
            if child.children[0] == name:
                return child
    return None # replace by an error ?

@addToClass(ast.JnxGetNode)
def interpret(self):
    value = getValFromAttributeName(self, "name")
    return vars[value]

@addToClass(ast.JnxVarNode)
def interpret(self):
    value = getValFromAttributeName(self, "name")
    vars[value] = []

@addToClass(ast.JnxForeachNode)
def interpret(self):
    output = ""
    collectionName = getValFromAttributeName(self, "in")
    itName = getValFromAttributeName(self, "name")

    for it in vars[collectionName]:
        vars[itName] = it
        self.chidren[0].interpret()

@addToClass(ast.JnxValueNode)
def interpret(self):
    if lastVar==None:
        pass # shutout error value is not in a var balise
    vars[lastVar].append(self.children[1])

@addToClass(ast.JnxForNode)
def interpret(self):
    pass

if __name__ == "__main__":
    prog = open(sys.argv[1]).read()
    ast = parse(prog)
    compiled = ast.interpret()

    fileWithoutPath = sys.argv[1].split('\\')[-1]
    fileWithoutExtension = os.path.splitext(fileWithoutPath)[0]
    name = os.getcwd() + "\\output\\XML\\" + fileWithoutExtension + ".xml"
    outfile = open(name,'w')
    outfile.write(compiled)
    outfile.close()

    print("Wrote output to",name)
