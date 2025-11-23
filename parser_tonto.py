import ply.yacc as yacc
from lexer_tonto import tokens, build_lexer

# --------------------------
#   Estrutura de síntese
# --------------------------
ontologia = {
    "packages": [],
    "classes": [],
    "datatypes": [],
    "enums": [],
    "generalizations": [],
    "relations_internal": [],
    "relations_external": [],
}

# --------------------------
def p_error(p):
    if p:
        print(f"[ERRO] Síntaxe inválida perto de '{p.value}' na linha {p.lineno}")
    else:
        print("[ERRO] Fim inesperado do arquivo (EOF).")

# ===============================================================
#   REGRA INICIAL
# ===============================================================

def p_start(p):
    """start : package"""
    p[0] = p[1]


# ===============================================================
#   1. DECLARAÇÃO DE PACOTES
# ===============================================================

def p_package(p):
    """package : PACKAGE IDENT LBRACE package_body RBRACE
               | PACKAGE CLASS_NAME LBRACE package_body RBRACE"""
    ontologia["packages"].append(p[2])
    p[0] = ("package", p[2], p[4])



def p_package_body(p):
    """package_body : package_item_list
                    | empty"""
    p[0] = p[1]


def p_package_item_list(p):
    """package_item_list : package_item_list package_item
                         | package_item"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[2])
        p[0] = p[1]


def p_package_item(p):
    """package_item : enum_decl
                    | class_decl
                    | datatype_decl
                    | generalization
                    | relation_external"""
    #p[0] = p[1]


# ===============================================================
#   2. DECLARAÇÃO DE CLASSES
# ===============================================================

def p_class_decl(p):
    """class_decl : CLASS_NAME COLON IDENT class_block"""
    ontologia["classes"].append({"name": p[1], "stereotype": p[3]})
    p[0] = ("class", p[1])


def p_class_block(p):
    """class_block : LBRACE class_body RBRACE
                   | empty"""
    pass


def p_class_body(p):
    """class_body : class_body class_element
                  | class_element"""
    pass


def p_class_element(p):
    """class_element : attribute
                     | relation_internal"""
    p[0] = p[1]


def p_attribute(p):
    """attribute : RELATION_NAME COLON IDENT
                 | RELATION_NAME COLON CLASS_NAME
                 | RELATION_NAME COLON NATIVE_TYPE
                 | RELATION_NAME COLON NEW_DATATYPE"""
    p[0] = ("attribute", p[1], p[3])


# ===============================================================
#   3. DECLARAÇÃO DE TIPOS DE DADOS
# ===============================================================

def p_datatype_decl(p):
    """datatype_decl : NEW_DATATYPE LBRACE attr_list RBRACE"""
    ontologia["datatypes"].append(p[1])
    p[0] = ("datatype", p[1])


def p_attr_list(p):
    """attr_list : attribute
                 | attr_list attribute"""
    pass

# ===============================================================
#   4. DECLARAÇÃO DE ENUMERATED CLASSES
# ===============================================================

def p_enum_decl(p):
    """enum_decl : ENUM CLASS_NAME LBRACE enum_items RBRACE"""
    ontologia["enums"].append(p[2])
    p[0] = ("enum", p[2])


def p_enum_item(p):
    """enum_item : CLASS_NAME
                 | IDENT"""
    p[0] = p[1]

def p_enum_items(p):
    """enum_items : enum_item
                  | enum_items enum_item"""

# ===============================================================
#   5. GENERALIZAÇÕES (GENSET)
# ===============================================================

def p_generalization(p):
    """generalization : CLASS_NAME CLASS_NAME genset_block"""
    ontologia["generalizations"].append(p[1])
    p[0] = ("genset", p[1])


def p_genset_block(p):
    """genset_block : LBRACE genset_body RBRACE"""
    p[0] = p[2]


def p_genset_body(p):
    """genset_body : IDENT COLON IDENT
                   | IDENT COLON IDENT COMMA IDENT"""
    p[0] = ("genset_body",)

# ===============================================================
#   6. RELAÇÕES
# ===============================================================

def p_relation_internal(p):
    """relation_internal : IDENT LBRACKET RANGE_DOTS RBRACKET LEFT_ARROW LBRACKET RANGE_DOTS RBRACKET CLASS_NAME"""
    ontologia["relations_internal"].append(p[1])
    p[0] = ("relation_internal", p[1])


def p_relation_external(p):
    """relation_external : AT IDENT IDENT CLASS_NAME RIGHT_ARROW CLASS_NAME"""
    ontologia["relations_external"].append(p[2])
    p[0] = ("relation_external", p[2])


# ===============================================================
def p_empty(p):
    """empty :"""
    pass


# ===============================================================
def build_parser():
    lexer = build_lexer()
    parser = yacc.yacc(debug=False)
    parser.lexer = lexer       
    return parser

# ===============================================================
# Teste rápido
# ===============================================================
if _name_ == "_main_":
    code = """
    package MyPkg {
        Person : kind {
            name : string
        }

        enum EyeColor {
            Blue Green Brown
        }
    }
    """

    parser = build_parser()
    parser.parse(code)
    print("\nSAÍDA FINAL:")
    print(ontologia)

