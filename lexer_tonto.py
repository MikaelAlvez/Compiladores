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
    "genset","disjoint","complete","general","specifics","where","import","functional-complexes","enum"
}

NATIVE_TYPES = {"number","string","boolean","date","time","datetime"}
META_ATTRIBUTES = {"ordered","const","derived","subsets","redefines"}

# --- lista de tokens do PLY ---
tokens = [
    'CLASS_NAME', 'RELATION_NAME', 'INSTANCE_NAME', 'NEW_DATATYPE',
    'NATIVE_TYPE', 'META_ATTRIBUTE',
    'NUMBER', 'STRING', 'BOOLEAN_LITERAL',
    'LBRACE','RBRACE','LPAREN','RPAREN','LBRACKET','RBRACKET',
    'RANGE_DOTS','LEFT_ARROW','RIGHT_ARROW','STAR','AT','COLON',
    'PACKAGE',
    'ENUM',
    'IDENT',
    'COMMA',
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
t_COMMA = r','

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
    t = classify_token(t)
    return t
    
def t_NATIVE_TYPE(t):
    r'\b(number|string|boolean|date|time|datetime)\b'
    return t

def t_ENUM(t):
    r'enum'
    return t


# Relation names: inicia com minúscula, seguido de letras ou underscores (sem dígitos)
def t_RELATION_NAME(t):
    r'\b[a-z][A-Za-z_]*\b'
    t = classify_token(t)
    return t


# fallback identifier (qualquer outro identificador)
def t_IDENT(t):
    r'\b[A-Za-z_][A-Za-z0-9_]*\b'
    t = classify_token(t)
    return t


# acompanhando linhas e colunas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    # não retorna token

    # erro
def t_error(t):
    col = find_column(t.lexer.lexdata, t)
    msg = f"Lexical error: caractere inválido '{t.value[0]}' na linha {t.lineno}, coluna {col}"
    # Sugestão simples: se for dígito em nome, indique convenção
    suggestion = ""
    if re.match(r'\d', t.value[0]):
        suggestion = " (verifique convenções de nomes/instâncias)."
    print(msg + suggestion)
    t.lexer.skip(1)

def find_column(input, token):
    last_cr = input.rfind('\n', 0, token.lexpos)
    if last_cr < 0:
        last_cr = -1
    return (token.lexpos - last_cr)

# --- utilitário para classificar tokens que precisam de distinção semântica ---
def classify_token(t):
    val = t.value
    lower = val.lower()

    # Palavra-chave PACKAGE
    if lower == "package":
        t.type = "PACKAGE"
        return t

    # Estereótipos de classes
    if lower in STEREOTYPE_CLASSES:
        t.type = 'IDENT'
        t.stype = 'STEREOTYPE_CLASS'
        return t

    # Estereótipos de relações
    if lower in STEREOTYPE_RELATIONS:
        t.type = 'IDENT'
        t.stype = 'STEREOTYPE_RELATION'
        return t

    # Palavras reservadas
    if lower in RESERVED_WORDS:
        t.type = 'IDENT'
        t.stype = 'RESERVED_WORD'
        return t

    # Tipos nativos
    if lower in NATIVE_TYPES:
        t.type = 'NATIVE_TYPE'
        return t

    # Meta-atributos
    if lower in META_ATTRIBUTES:
        t.type = 'META_ATTRIBUTE'
        return t

    return t

# função principal de tokenização que aplica classificação extra
def build_lexer(**kwargs):
    lexer = lex.lex(module=sys.modules[__name__], **kwargs)
    return lexer

# função que percorre e retorna lista analítica + síntese
def analyze(text):
    lexer = build_lexer()
    lexer.input(text)
    tokens_out = []
    summary = Counter()
    # contadores detalhados
    counters = defaultdict(int)

    while True:
        tok = lexer.token()
        if not tok:
            break
        # calcular coluna
        col = find_column(lexer.lexdata, tok)
        # classificação adicional
        if tok.type in ("CLASS_NAME","RELATION_NAME","INSTANCE_NAME","NEW_DATATYPE","RELATION_NAME"):
            tok = classify_token(tok)
        # marcação de estereótipo/reserved/etc.
        stype = getattr(tok, 'stype', None)
        if stype == 'STEREOTYPE_CLASS':
            counters['stereotype_class'] += 1
        elif stype == 'STEREOTYPE_RELATION':
            counters['stereotype_relation'] += 1
        elif stype == 'RESERVED_WORD':
            counters['reserved_word'] += 1
        elif tok.type == 'NATIVE_TYPE':
            counters['native_type'] += 1
        elif tok.type == 'META_ATTRIBUTE':
            counters['meta_attribute'] += 1
        elif tok.type == 'INSTANCE_NAME':
            counters['instance'] += 1
        elif tok.type == 'CLASS_NAME':
            counters['class_name'] += 1
        elif tok.type == 'RELATION_NAME':
            counters['relation_name'] += 1

        # salvar token com posição
        tokens_out.append({
            'type': tok.type,
            'value': tok.value,
            'line': tok.lineno,
            'col': col,
            'subtype': stype
        })
        
    # montar síntese pedida no enunciado
    summary_table = {
        'classes': counters.get('class_name', 0) + counters.get('stereotype_class', 0),
        'relations': counters.get('relation_name', 0) + counters.get('stereotype_relation', 0),
        'words_reserved': counters.get('reserved_word', 0),
        'instances': counters.get('instance', 0),
        'native_types': counters.get('native_type', 0),
        'meta_attributes': counters.get('meta_attribute', 0)
    }
    return tokens_out, summary_table                                                                        

# --- se executado diretamente faz um teste rápido ---
if __name__ == "__main__":
    sample = '''
    package mypkg {
      Person : kind
      hasParent : material
      Planeta1 : Person
      CPFDataType
      number
      ordered
      "uma string de teste"
      true
      <>-- --<>
    }
    '''
    toks, synth = analyze(sample)
    print("Tokens:")
    for t in toks:
        print(f"{t['line']:3}:{t['col']:3}  {t['type']:15} {t['value']} {('['+t['subtype']+']') if t['subtype'] else ''}")
    print("\nSíntese:", synth)
