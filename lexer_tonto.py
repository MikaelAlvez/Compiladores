# lexer_tonto.py
import re
import sys
import ply.lex as lex
from collections import Counter, defaultdict

# --- listas conforme especificação ---
STEREOTYPE_CLASSES = {
    "event","situation","process","category","mixin","phaseMixin","roleMixin",
    "historicalRoleMixin","kind","collective","quantity","quality","mode",
    "intrisicMode","extrinsicMode","subkind","phase","role","historicalRole"
}

STEREOTYPE_RELATIONS = {
    "material","derivation","comparative","mediation","characterization",
    "externalDependence","componentOf","memberOf","subCollectionOf","subQualityOf",
    "instantiation","termination","participational","participation",
    "historicalDependence","creation","manifestation","bringsAbout","triggers",
    "composition","aggregation","inherence","value","formal","constitution"
}

RESERVED_WORDS = {
    "genset","disjoint","complete","general","specifics","where","package","import","functional-complexes"
}

NATIVE_TYPES = {"number","string","boolean","date","time","datetime"}
META_ATTRIBUTES = {"ordered","const","derived","subsets","redefines"}

# --- lista de tokens do PLY ---
tokens = [
    # palavras-chave específicas e estereótipos (tratadas em t_ID)
    'CLASS_NAME', 'RELATION_NAME', 'INSTANCE_NAME', 'NEW_DATATYPE',
    'NATIVE_TYPE', 'META_ATTRIBUTE',
    'NUMBER', 'STRING', 'BOOLEAN_LITERAL',
    # símbolos
    'LBRACE','RBRACE','LPAREN','RPAREN','LBRACKET','RBRACKET',
    'RANGE_DOTS','LEFT_ARROW','RIGHT_ARROW','STAR','AT','COLON',
    'IDENT'  # fallback para identificadores que não se encaixam
]

# regex para símbolos complexos primeiro
t_RANGE_DOTS = r'\.\.'
t_LEFT_ARROW = r'\<\>\--'   # "<>--"
t_RIGHT_ARROW = r'\--\<\>'  # "--<>"
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_STAR = r'\*'
t_AT = r'@'
t_COLON = r':'

t_ignore = ' \t\r'  # espaços e tabs