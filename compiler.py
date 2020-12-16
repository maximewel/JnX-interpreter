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
    output = f"<{currentTag}"
    if len(self.children) >= 2:
        output += f" {self.children[0].interpret()}"
    output += ">\n"
    
    return output

@addToClass(ast.BaliseEndNode)
def interpret(self):
    lastTag = tags.pop(0)
    if (lastTag != self.children[0]):
        pass # output error and exit

    return f"</{lastTag}>\n"

"""  ---- JINX-NODES ----   """
@addToClass(ast.JnxGetNode)
def interpret(self):
    return vars[self.]

@addToClass(ast.JnxVarNode)
def interpret(self):
    pass

@addToClass(ast.JnxForeachNode)
def interpret(self):
    pass

@addToClass(ast.JnxValueNode)
def interpret(self):
    pass

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
