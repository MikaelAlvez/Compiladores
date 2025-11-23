from parser_tonto import build_parser

parser = build_parser()

code = """
package MyPkg {
    Person : kind {
        name : string
    }
}
"""


print("=== PARSING ===")
result = parser.parse(code)
print("=== RESULTADO ===")
print(result)
