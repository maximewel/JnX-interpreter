
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftTRANSFORM_NODEATTRIB_VAL COMMENT IDENTIFIER JNX_TAG_END JNX_TAG_HEADER_END JNX_TAG_HEADER_START JNX_TAG_START document : jinx_header bloc \n    | bloc bloc : line %prec TRANSFORM_NODE \n    | inline %prec TRANSFORM_NODE \n    | line_jnx %prec TRANSFORM_NODE\n    | comment  bloc : bloc line\n    | bloc inline \n    | bloc line_jnx  line : balise_start token_sequence balise_end\n    | balise_start bloc balise_end  line_jnx : balise_start_jnx token_sequence balise_end_jnx\n    | balise_start_jnx bloc balise_end_jnx  line_jnx : balise_autoclose_jnx  inline : balise_autoclose  balise_autoclose : tag "/" ">"\n    | tag attributes "/" ">"  balise_autoclose_jnx : tag_jnx "/" ">"\n    | tag_jnx attributes "/" ">"  balise_start : tag ">"\n    | tag attributes ">" balise_start_jnx : tag_jnx ">"\n    | tag_jnx attributes ">" tag : "<" token  tag_jnx : JNX_TAG_START  jinx_header : JNX_TAG_HEADER_START attributes JNX_TAG_HEADER_END balise_end : "<" "/" token  ">"  balise_end_jnx : "<" JNX_TAG_END  comment : COMMENT  attributes : attribute \n    | attributes attribute attribute : token "=" ATTRIB_VAL  token : IDENTIFIER  token_sequence : token\n    | token_sequence token '
    
_lr_action_items = {'JNX_TAG_HEADER_START':([0,],[4,]),'COMMENT':([0,2,9,11,31,34,38,50,53,],[13,13,13,13,-20,-22,-26,-21,-23,]),'<':([0,2,3,5,6,7,8,9,10,11,12,13,18,19,20,21,25,26,27,28,29,30,31,34,38,41,42,44,46,48,50,52,53,55,58,59,60,62,],[16,16,16,-3,-4,-5,-6,16,-15,16,-14,-29,16,-7,-8,-9,-33,43,45,-34,47,49,-20,-22,-26,-10,-35,-11,-12,-13,-21,-16,-23,-18,-28,-17,-19,-27,]),'JNX_TAG_START':([0,2,3,5,6,7,8,9,10,11,12,13,18,19,20,21,27,30,31,34,38,41,44,46,48,50,52,53,55,58,59,60,62,],[17,17,17,-3,-4,-5,-6,17,-15,17,-14,-29,17,-7,-8,-9,17,17,-20,-22,-26,-10,-11,-12,-13,-21,-16,-23,-18,-28,-17,-19,-27,]),'$end':([1,3,5,6,7,8,10,12,13,18,19,20,21,41,44,46,48,52,55,58,59,60,62,],[0,-2,-3,-4,-5,-6,-15,-14,-29,-1,-7,-8,-9,-10,-11,-12,-13,-16,-18,-28,-17,-19,-27,]),'IDENTIFIER':([4,9,11,14,15,16,17,22,23,25,26,28,29,31,32,34,35,37,39,42,45,49,50,53,56,57,],[25,25,25,25,25,25,-25,25,-30,-33,25,-34,25,-20,25,-22,25,-24,-31,-35,25,25,-21,-23,-32,25,]),'>':([14,15,17,23,25,32,33,35,36,37,39,51,54,56,61,],[31,34,-25,-30,-33,50,52,53,55,-24,-31,59,60,-32,62,]),'/':([14,15,17,23,25,32,35,37,39,43,45,56,],[33,36,-25,-30,-33,51,54,-24,-31,57,57,-32,]),'JNX_TAG_HEADER_END':([22,23,39,56,],[38,-30,-31,-32,]),'=':([24,25,],[40,-33,]),'ATTRIB_VAL':([40,],[56,]),'JNX_TAG_END':([47,49,],[58,58,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'document':([0,],[1,]),'jinx_header':([0,],[2,]),'bloc':([0,2,9,11,],[3,18,27,30,]),'line':([0,2,3,9,11,18,27,30,],[5,5,19,5,5,19,19,19,]),'inline':([0,2,3,9,11,18,27,30,],[6,6,20,6,6,20,20,20,]),'line_jnx':([0,2,3,9,11,18,27,30,],[7,7,21,7,7,21,21,21,]),'comment':([0,2,9,11,],[8,8,8,8,]),'balise_start':([0,2,3,9,11,18,27,30,],[9,9,9,9,9,9,9,9,]),'balise_autoclose':([0,2,3,9,11,18,27,30,],[10,10,10,10,10,10,10,10,]),'balise_start_jnx':([0,2,3,9,11,18,27,30,],[11,11,11,11,11,11,11,11,]),'balise_autoclose_jnx':([0,2,3,9,11,18,27,30,],[12,12,12,12,12,12,12,12,]),'tag':([0,2,3,9,11,18,27,30,],[14,14,14,14,14,14,14,14,]),'tag_jnx':([0,2,3,9,11,18,27,30,],[15,15,15,15,15,15,15,15,]),'attributes':([4,14,15,],[22,32,35,]),'attribute':([4,14,15,22,32,35,],[23,23,23,39,39,39,]),'token':([4,9,11,14,15,16,22,26,29,32,35,45,49,57,],[24,28,28,24,24,37,24,42,42,24,24,37,37,61,]),'token_sequence':([9,11,],[26,29,]),'balise_end':([26,27,],[41,44,]),'balise_end_jnx':([29,30,],[46,48,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> document","S'",1,None,None,None),
  ('document -> jinx_header bloc','document',2,'p_document','parserast.py',23),
  ('document -> bloc','document',1,'p_document','parserast.py',24),
  ('bloc -> line','bloc',1,'p_bloc','parserast.py',31),
  ('bloc -> inline','bloc',1,'p_bloc','parserast.py',32),
  ('bloc -> line_jnx','bloc',1,'p_bloc','parserast.py',33),
  ('bloc -> comment','bloc',1,'p_bloc','parserast.py',34),
  ('bloc -> bloc line','bloc',2,'p_bloc_multiple','parserast.py',38),
  ('bloc -> bloc inline','bloc',2,'p_bloc_multiple','parserast.py',39),
  ('bloc -> bloc line_jnx','bloc',2,'p_bloc_multiple','parserast.py',40),
  ('line -> balise_start token_sequence balise_end','line',3,'p_line','parserast.py',44),
  ('line -> balise_start bloc balise_end','line',3,'p_line','parserast.py',45),
  ('line_jnx -> balise_start_jnx token_sequence balise_end_jnx','line_jnx',3,'p_line_jnx','parserast.py',59),
  ('line_jnx -> balise_start_jnx bloc balise_end_jnx','line_jnx',3,'p_line_jnx','parserast.py',60),
  ('line_jnx -> balise_autoclose_jnx','line_jnx',1,'p_line_autoclose_jnx','parserast.py',71),
  ('inline -> balise_autoclose','inline',1,'p_inline','parserast.py',75),
  ('balise_autoclose -> tag / >','balise_autoclose',3,'p_auto_balise','parserast.py',85),
  ('balise_autoclose -> tag attributes / >','balise_autoclose',4,'p_auto_balise','parserast.py',86),
  ('balise_autoclose_jnx -> tag_jnx / >','balise_autoclose_jnx',3,'p_auto_balise_jnx','parserast.py',93),
  ('balise_autoclose_jnx -> tag_jnx attributes / >','balise_autoclose_jnx',4,'p_auto_balise_jnx','parserast.py',94),
  ('balise_start -> tag >','balise_start',2,'p_balise_start','parserast.py',101),
  ('balise_start -> tag attributes >','balise_start',3,'p_balise_start','parserast.py',102),
  ('balise_start_jnx -> tag_jnx >','balise_start_jnx',2,'p_balise_start_jnx','parserast.py',109),
  ('balise_start_jnx -> tag_jnx attributes >','balise_start_jnx',3,'p_balise_start_jnx','parserast.py',110),
  ('tag -> < token','tag',2,'p_tag','parserast.py',118),
  ('tag_jnx -> JNX_TAG_START','tag_jnx',1,'p_tag_jinx','parserast.py',122),
  ('jinx_header -> JNX_TAG_HEADER_START attributes JNX_TAG_HEADER_END','jinx_header',3,'p_jinx_header','parserast.py',130),
  ('balise_end -> < / token >','balise_end',4,'p_balise_end','parserast.py',134),
  ('balise_end_jnx -> < JNX_TAG_END','balise_end_jnx',2,'p_balise_end_jinx','parserast.py',138),
  ('comment -> COMMENT','comment',1,'p_comment','parserast.py',146),
  ('attributes -> attribute','attributes',1,'p_attributes_sequence','parserast.py',152),
  ('attributes -> attributes attribute','attributes',2,'p_attributes_sequence','parserast.py',153),
  ('attribute -> token = ATTRIB_VAL','attribute',3,'p_attribute','parserast.py',160),
  ('token -> IDENTIFIER','token',1,'p_token','parserast.py',166),
  ('token_sequence -> token','token_sequence',1,'p_token_sequence','parserast.py',170),
  ('token_sequence -> token_sequence token','token_sequence',2,'p_token_sequence','parserast.py',171),
]
