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

