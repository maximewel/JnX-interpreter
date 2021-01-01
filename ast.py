# coding: latin-1

''' Petit module utilitaire pour la construction, la manipulation et la 
repr�sentation d'arbres syntaxiques abstraits.

S�rement plein de bugs et autres surprises. � prendre comme un 
"work in progress"...
Notamment, l'utilisation de pydot pour repr�senter un arbre syntaxique cousu
est une utilisation un peu "limite" de graphviz. �a marche, mais le layout n'est
pas toujours optimal...
'''

import pydot

class Node:
    count = 0
    type = 'Node (unspecified)'
    shape = 'ellipse'
    def __init__(self,children=None):
        self.ID = str(Node.count)
        Node.count+=1
        if not children: self.children = []
        elif hasattr(children,'__len__'):
            self.children = children
        else:
            self.children = [children]
        self.next = []

    def addNext(self,next):
        self.next.append(next)

    def asciitree(self, prefix=''):
        result = "%s%s\n" % (prefix, repr(self))
        prefix += '|  '
        for c in self.children:
            if not isinstance(c,Node):
                result += "%s*** Error: Child of type %r: %r\n" % (prefix,type(c),c)
                continue
            result += c.asciitree(prefix)
        return result
    
    def __str__(self):
        return self.asciitree()
    
    def __repr__(self):
        return self.type
    
    def makegraphicaltree(self, dot=None, edgeLabels=True):
            if not dot: dot = pydot.Dot()
            dot.add_node(pydot.Node(self.ID,label=repr(self), shape=self.shape))
            label = edgeLabels and len(self.children)-1
            for i, c in enumerate(self.children):
                c.makegraphicaltree(dot, edgeLabels)
                edge = pydot.Edge(self.ID,c.ID)
                if label:
                    edge.set_label(str(i))
                dot.add_edge(edge)
                #Workaround for a bug in pydot 1.0.2 on Windows:
                #dot.set_graphviz_executables({'dot': r'C:\Program Files\Graphviz2.38\bin\dot.exe'})
            return dot
        
class DocumentNode(Node):
    type = 'Document'

class TokenNode(Node):
    type = 'token'
    def __init__(self, tok):
        Node.__init__(self)
        self.tok = tok
        
    def __repr__(self):
        return repr(self.tok)

class InfoNode(Node):
    type = 'Info'

class AttributeNode(Node):
    type = '='
    
class BlocNode(Node):
    type='bloc'
    def __init__(self, nodes, tag, info=None):
        Node.__init__(self, nodes)
        self.tag = tag
        self.info = info
    
    def __repr__(self):
        base = Node.__repr__(self) 
        return f"{base} : {self.tag}"

class InlineNode(BlocNode):
    type='inline'
    def __init__(self, tag, info=None):
        BlocNode.__init__(self, [], tag, info)

class JnxLineNode(Node):
    type='jnxLine'

class JnxHeader(Node):
    type='header'

class JnxGetNode(Node):
    type='jnx:get'
    def __init__(self, name):
        Node.__init__(self, None)
        self.name = name
    
    def __repr__(self):
        base = Node.__repr__(self) 
        return f"{base}({self.name})"

class JnxVarNode(Node):
    type='jnx:var'
    def __init__(self, children, name):
        Node.__init__(self, children)
        self.name = name
    
    def __repr__(self):
        base = Node.__repr__(self) 
        return f"{base}({self.name})"
class JnxForeachNode(Node):
    type='jnx:foreach'
    def __init__(self, nodes, itName, collecName):
        Node.__init__(self, nodes)
        self.itName = itName
        self.collecName = collecName
    
    def __repr__(self):
        base = Node.__repr__(self) 
        return f"{base}({self.itName} in {self.collecName})"

class JnxValueNode(Node):
    type='jnx:value'
    def __init__(self, value):
        Node.__init__(self, None)
        self.value = value
    
    def __repr__(self):
        base = Node.__repr__(self) 
        return f"{base}({self.value})"

class JnxForNode(Node):
    type='jnx:for'
    def __init__(self, nodes, start, to, step, itName):
        Node.__init__(self, nodes)
        self.start = start
        self.to = to
        self.step=step
        self.itName = itName
    
    def __repr__(self):
        base = Node.__repr__(self) 
        return f"{base}({self.start} to {self.to} by {self.step})"

class CommentNode(Node):
    type = 'comment'
    def __init__(self, comment):
        Node.__init__(self)
        self.comment = comment
        
    def __repr__(self):
        return repr("comment : " + self.comment)
    
def addToClass(cls):
    ''' D�corateur permettant d'ajouter la fonction d�cor�e en tant que m�thode
    � une classe.
    
    Permet d'impl�menter une forme �l�mentaire de programmation orient�e
    aspects en regroupant les m�thodes de diff�rentes classes impl�mentant
    une m�me fonctionnalit� en un seul endroit.
    
    Attention, apr�s utilisation de ce d�corateur, la fonction d�cor�e reste dans
    le namespace courant. Si cela d�range, on peut utiliser del pour la d�truire.
    Je ne sais pas s'il existe un moyen d'�viter ce ph�nom�ne.
    '''
    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator
