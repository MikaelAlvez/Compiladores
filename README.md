# `lexer_tonto.py` - Analisador Léxico (Lexer)

Este script Python implementa um **Analisador Léxico (Lexer)** utilizando a biblioteca **PLY (Python Lex-Yacc)** para a linguagem OntoUML ou uma variação inspirada nela, conforme as regras de nomenclatura e lista de palavras-chave/estereótipos definidas no código.

## 🎯 Objetivo

O principal objetivo deste lexer é:

1.  **Tokenizar** uma *string* de entrada (código-fonte) em uma sequência de *tokens*.
2.  **Classificar semanticamente** os identificadores (IDs) de acordo com convenções de nomenclatura e listas pré-definidas (palavras reservadas, estereótipos, tipos nativos, etc.).
3.  Gerar uma **análise detalhada** da lista de tokens encontrados, incluindo informações de linha e coluna.
4.  Fornecer uma **síntese** da contagem de elementos principais.

## 🛠️ Requisitos

O script requer a biblioteca **PLY** para a geração do analisador léxico.

### Instalação

```bash
pip install ply