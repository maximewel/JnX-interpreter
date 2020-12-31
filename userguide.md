# Guide utilisateur JNX
Ceci est le guide utilisateur de JNX, les sections suivantes expliqueront comment installer les pré-requis pour lancer notre interpreteur, ainsi que des exemples de lancement.

## Pré-requis
La bonne éxecution des étapes qui vont suivre requiert l'installation des composants suivants :

(Pour que le module Pydot puisse fonctionner correctement il faut que [Graphiz](https://graphviz.org/) soit installé préalablement sur la machine !)

* Python 3.8 avec les modules : 
  * [PLY](https://www.dabeaz.com/ply/) version 3.11
    * installation avec pip : `pip install ply`
  * [Pydot]()
    * Installation avec pip : `pip install pydot`

## Installation 
Il n'y pas de procédure d'installation spécifique pour executer notre interpréteur, il suffit de reprendre le dossier contenant les scripts python et si les dépendances sont correctement installées, tout devrait fonctionner.

Il suffit simplement de récupérer les sources depuis github, par exemple via une clone : 

> git clone https://github.com/maximewel/JnX-interpreter.git

## Exécution
Plusieurs commandes sont disponibles selon ce que l'on souhaite obtenir

> `python lex.py fileInput.jnx`
 
Permet d'effectuer une analyse lexicale, la sortie de l'analyse lexicale est disponible sous le dossier `generated`

> `python parserast.py fileInput.jnx` 

Permet de faire une analyse syntaxique ainsi que de faire la construction de l'AST, cette commande génére un graphe de sortie sous format pdf avec le nom du fichier d'entré ex. fileInput.jnx

> `python compiler.py fileInput.jnx` 

Permet d'effectuer l'interprétation des fichiers jnx, cette commande générera un fichier xml avec le nom du fichier entré ex. fileInput.xml

Des fichiers d'exemples sont disponibles dans le dossier data