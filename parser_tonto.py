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

