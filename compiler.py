import ast
from ast import addToClass
from functools import reduce
from parserast import parse
import sys
import os

# pylint: disable=function-redefined


""" --- init variables --- """
vars = {}

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

@addToClass(ast.DocumentNode)
def interpret(self):
    xmlDocument = ""
    for c in self.children:
        xmlDocument += c.interpret()
    return xmlDocument

@addToClass(ast.LineNode)
def interpret(self):
    return self.children.interpret()

@addToClass(ast.BlocNode)
def interpret(self):
    xml = ""
    return xml

if __name__ == "__main__":
    prog = open(sys.argv[1]).read()
    ast = parse(prog)
    compiled = ast.compile()

    fileWithoutPath = sys.argv[1].split('\\')[-1]
    fileWithoutExtension = os.path.splitext(fileWithoutPath)[0]
    name = os.getcwd() + "\\output\\XML\\" + fileWithoutExtension + ".xml"
    outfile = open(name,'w')
    outfile.write(compiled)
    outfile.close()

    print("Wrote output to",name)
