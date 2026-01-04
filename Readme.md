# Token
INT, IF, ELSE, WHILE, FOR,
    ID, NUMBER,
    PLUS, MINUS, MUL, DIV,
    ASSIGN, EQ, LT, GT,
    LPAREN, RPAREN,
    LBRACE, RBRACE,
    SEMI,
    END

KEYWORDS: int if else while for
SYMBOLS: ( ) { } ; =
OPERATORS: + - * / < > <= >= == !=
IDENTIFIER: variable names
INTEGER: numbers
EOF

#####
# parser
# done program
    → statement*

statement
    → declaration
    | assignment ";"
    | if_statement
    | while_statement
    | for_statement
    | block
    | empty

block
    → "{" statement* "}"

# done declaration
    → "int" IDENT ";"

# done assignment
    → IDENT "=" expr

# done if_statement
    → "if" "(" expr ")" block
      ("else" "if" "(" expr ")" block)*
      ("else" block)?

# done while_statement
    → "while" "(" expr ")" block

# done for_statement
    → "for" "(" assignment ";" expr ";" assignment ")" block

# done expr
    → equality_expr

# done equality_expr
    → comparison_expr (( "==" | "!=" ) comparison_expr)?

# done comparison_expr
    → arithmetic_expr (( "<" | ">" | "<=" | ">=" ) arithmetic_expr)?

# done arithmetic_expr
    → term (( "+" | "-" ) term)*

# done term    
    → factor (( "*" | "/" ) factor)*

empty
    → ε

