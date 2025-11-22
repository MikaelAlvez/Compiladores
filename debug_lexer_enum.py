from lexer_tonto import build_lexer

lexer = build_lexer()
lexer.input("enum EyeColor { Blue Green Brown }")

while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok.type, tok.value)
