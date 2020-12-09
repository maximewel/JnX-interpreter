import ast
from ast import addToClass
from functools import reduce
from parserast import parse
import sys
import os


""" --- init variables --- """
vars = {}

""" --- Nodes gestion ---"""

"""         ---- XML-Structure-Nodes ----
DocumentNode
TokenNode
LineNode
BlocNode
""" """     ---- LINES-Nodes ----
InfoNode
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

@addToClass(ast.ProgramNode)
def compile(self):
    bytecode = ""
    for c in self.children:
        bytecode += c.compile()
    return bytecode

@addToClass(ast.TokenNode)
def compile(self):
    bytecode = ""
    if isinstance(self.tok, str):
        bytecode += "PUSHV %s\n" % self.tok
    else:
        bytecode += "PUSHC %s\n" % self.tok
    return bytecode

@addToClass(ast.AssignNode)
def compile(self):
    bytecode = ""
    bytecode += self.children[1].compile()
    bytecode += "SET %s\n" % self.children[0].tok
    return bytecode
    
@addToClass(ast.PrintNode)
def compile(self):
    bytecode = ""
    bytecode += self.children[0].compile()
    bytecode += "PRINT\n"
    return bytecode
    
@addToClass(ast.OpNode)
def compile(self):
    bytecode = ""
    if len(self.children) == 1:
        bytecode += self.children[0].compile()
        bytecode += "USUB\n"
    else:
        for c in self.children:
            bytecode += c.compile()
        bytecode += ops[self.op] + "\n"
    return bytecode
    
@addToClass(ast.WhileNode)
def compile(self):
    bytecode = ""
    bytecode += "JMP cond%s\n" % counter
    bytecode += "body%s: " % counter
    bytecode += self.children[1].compile()
    bytecode += "cond%s: " % counter
    bytecode += self.children[0].compile()
    bytecode += "JINZ body%s\n" % counter
    return bytecode

if __name__ == "__main__":
    prog = open(sys.argv[1]).read()
    ast = parse(prog)
    compiled = ast.compile()

    fileWithoutPath = sys.argv[1].split('\\')[-1]
    fileWithoutExtension = os.path.splitext(fileWithoutPath)[0]
    filenameOutput = os.getcwd() + "\\output\\XML\\" + fileWithoutExtension + ".JnX"
    outfile = open(name,'w')
    outfile.write(compiled)
    outfile.close()

    print("Wrote output to",name)
