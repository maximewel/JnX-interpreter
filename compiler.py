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
"""         ---- XML-Nodes ----
DocumentNode
BlocNode
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

@addToClass(ast.BlocNode)
def interpret(self):
    global countLines
    output = "\t"*countLines + f"<{self.tag}"
    if self.info:
        output += self.info.interpret()
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
    global countLines
    output = "\t"*countLines + f"<{self.tag}"
    if self.info:
        output += self.info.interpret()
    output += "/>\n"

    return output

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
@addToClass(ast.JnxGetNode)
def interpret(self):
    value = self.name
    return "\t"*countLines + str(vars[value]) + "\n"

@addToClass(ast.JnxVarNode)
def interpret(self):
    global lastVar
    name = self.name
    vars[name] = []
    lastVar = name
    output = ""

    if len(self.children):
        for c in self.children:
            output += c.interpret()

    return output

@addToClass(ast.JnxValueNode)
def interpret(self):
    global lastVar
    vars[lastVar].append(self.value)
    return ""

@addToClass(ast.JnxForeachNode)
def interpret(self):
    output = ""

    for it in vars[self.collecName]:
        vars[self.itName] = it
        output += interpretChildren(self)

    return output

@addToClass(ast.JnxForNode)
def interpret(self):
    output = ""

    for it in range(self.start, self.to, self.step):
        vars[self.itName] = it
        output += interpretChildren(self)

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
