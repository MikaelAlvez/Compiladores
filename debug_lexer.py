from lexer_tonto import build_lexer

code = "package MyPkg { }"

lexer = build_lexer()
lexer.input(code)

for tok in lexer:
    print(f"type={tok.type:<10} value={tok.value:<10} subtype={getattr(tok,'stype',None)}")
