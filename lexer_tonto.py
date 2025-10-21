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

# Strings entre "..."
def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    # remove as aspas
    t.value = t.value[1:-1]
    return t

# Número inteiro ou real
def t_NUMBER(t):
    r'\d+(\.\d+)?'
    if '.' in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t

# boolean literal lowercase true/false
def t_BOOLEAN_LITERAL(t):
    r'\b(true|false)\b'
    t.value = True if t.value == 'true' else False
    return t

# New data type: letters only, terminando em DataType, sem números e sem underscores
def t_NEW_DATATYPE(t):
    r'\b[A-Za-z]+DataType\b'
    return t

# Instance names: termina com um inteiro (um ou mais dígitos)
# Permitir letras e underscores antes, mas obrigar a terminar em dígitos
def t_INSTANCE_NAME(t):
    r'\b[A-Za-z_][A-Za-z_]*\d+\b'
    return t

# Class names: inicia com Maiúscula, seguido de letras ou underscores (sem dígitos)
def t_CLASS_NAME(t):
    r'\b[A-Z][A-Za-z_]*\b'
    # evitar confundir com NEW_DATATYPE (já tratado acima)
    return t

# Relation names: inicia com minúscula, seguido de letras ou underscores (sem dígitos)
def t_RELATION_NAME(t):
    r'\b[a-z][A-Za-z_]*\b'
    # valor será analisado depois (poderá ser um estereótipo, reserved, native type, meta-attribute, etc.)
    return t

# fallback identifier (qualquer outro identificador)
def t_IDENT(t):
    r'\b[A-Za-z_][A-Za-z0-9_]*\b'
    return t

# acompanhando linhas e colunas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    # não retorna token