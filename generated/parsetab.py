
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftTRANSFORM_NODEATTRIB_VAL IDENTIFIER JNX_TAG document : bloc  bloc : line %prec TRANSFORM_NODE  bloc : bloc line  line : balise_start token balise_end\n    | balise_start bloc balise_end \n    | balise_autoclose balise_autoclose : tag "/" ">"\n    | tag attributes "/" ">"  balise_start : tag ">"\n    | tag attributes ">" tag : JNX_TAG\n    | "<" token  balise_end : "<" "/" token  ">"  attributes : attribute \n    | attributes attribute attribute : token "=" ATTRIB_VAL  token : IDENTIFIER '
    
_lr_action_items = {'JNX_TAG':([0,2,3,4,5,9,11,13,19,21,23,26,29,32,],[7,7,-2,7,-6,-3,7,-9,-4,-5,-10,-7,-8,-13,]),'<':([0,2,3,4,5,9,10,11,12,13,19,21,23,26,29,32,],[8,8,-2,8,-6,-3,20,22,-17,-9,-4,-5,-10,-7,-8,-13,]),'$end':([1,2,3,5,9,19,21,26,29,32,],[0,-1,-2,-6,-3,-4,-5,-7,-8,-13,]),'IDENTIFIER':([4,6,7,8,12,13,14,16,18,22,23,25,28,30,],[12,12,-11,12,-17,-9,12,-14,-12,12,-10,-15,12,-16,]),'>':([6,7,12,14,15,16,18,24,25,30,31,],[13,-11,-17,23,26,-14,-12,29,-15,-16,32,]),'/':([6,7,12,14,16,18,20,22,25,30,],[15,-11,-17,24,-14,-12,28,28,-15,-16,]),'=':([12,17,],[-17,27,]),'ATTRIB_VAL':([27,],[30,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'document':([0,],[1,]),'bloc':([0,4,],[2,11,]),'line':([0,2,4,11,],[3,9,3,9,]),'balise_start':([0,2,4,11,],[4,4,4,4,]),'balise_autoclose':([0,2,4,11,],[5,5,5,5,]),'tag':([0,2,4,11,],[6,6,6,6,]),'token':([4,6,8,14,22,28,],[10,17,18,17,18,31,]),'attributes':([6,],[14,]),'attribute':([6,14,],[16,25,]),'balise_end':([10,11,],[19,21,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> document","S'",1,None,None,None),
  ('document -> bloc','document',1,'p_document','parserast.py',23),
  ('bloc -> line','bloc',1,'p_bloc','parserast.py',27),
  ('bloc -> bloc line','bloc',2,'p_bloc_multiple','parserast.py',31),
  ('line -> balise_start token balise_end','line',3,'p_line','parserast.py',35),
  ('line -> balise_start bloc balise_end','line',3,'p_line','parserast.py',36),
  ('line -> balise_autoclose','line',1,'p_line','parserast.py',37),
  ('balise_autoclose -> tag / >','balise_autoclose',3,'p_autoBalise','parserast.py',46),
  ('balise_autoclose -> tag attributes / >','balise_autoclose',4,'p_autoBalise','parserast.py',47),
  ('balise_start -> tag >','balise_start',2,'p_balise_start','parserast.py',55),
  ('balise_start -> tag attributes >','balise_start',3,'p_balise_start','parserast.py',56),
  ('tag -> JNX_TAG','tag',1,'p_tag','parserast.py',63),
  ('tag -> < token','tag',2,'p_tag','parserast.py',64),
  ('balise_end -> < / token >','balise_end',4,'p_balise_end','parserast.py',71),
  ('attributes -> attribute','attributes',1,'p_attributes_sequence','parserast.py',76),
  ('attributes -> attributes attribute','attributes',2,'p_attributes_sequence','parserast.py',77),
  ('attribute -> token = ATTRIB_VAL','attribute',3,'p_attribute','parserast.py',84),
  ('token -> IDENTIFIER','token',1,'p_token','parserast.py',90),
]
