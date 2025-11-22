from lexer_tonto import build_lexer

lexer = build_lexer()
lexer.input("name : string")

while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok.type, tok.value)
