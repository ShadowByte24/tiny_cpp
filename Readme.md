# tinycpp 🧩  
A Tiny C++-like Language Interpreter written in Python

tinycpp is a **minimal C++-style language interpreter** implemented from scratch in Python.
It is designed as an educational project to understand how programming languages work internally.

This project demonstrates:
- Lexical analysis (tokenization)
- Recursive-descent parsing
- Abstract Syntax Tree (AST) construction
- AST-based interpretation (execution)

The syntax and structure are inspired by **C++**, but the language is intentionally simplified.

---

## ✨ Supported Language Features

### ✅ Data Types
- `int` (integer variables)

```md
### ✅ Statements

- Variable declaration  
  ```cpp
  int x;
````

* Assignment

  ```cpp
  x = 10;
  ```

* `if / else`

* `while` loop

* Block statements using `{ }`

### ✅ Expressions

* Arithmetic operators: `+ - * /`
* Comparison operators: `< > <= >=`
* Equality operators: `== !=`
* Parentheses for grouping

---

## 📌 Example tinycpp Program

```cpp
int x;
x = 0;

while (x < 5) {
    x = x + 1;
}
```

### Execution Result (Python Interpreter State)

```python
{'x': 5}
```

---

## 🏗 Project Architecture

```
tinycpp.py
│
├── Token           → Token representation
├── lexer           → Converts source code → tokens
├── AST Nodes       → Program, Block, Assign, BinOp, If, While
├── Parser          → Tokens → Abstract Syntax Tree (AST)
├── Interpreter     → Executes AST using visitor pattern
└── main            → Runs a sample tinycpp program
```

---

## 🧠 How tinycpp Works

### 1️⃣ Lexer (Tokenizer)

The lexer reads raw source code and converts it into tokens.

Example:

```cpp
int x;
```

Tokens:

```
INT  ID  SEMI
```

---

### 2️⃣ Parser

The parser uses **recursive-descent parsing** to convert tokens into an AST.

Example:

```cpp
x = x + 1;
```

AST (conceptual):

```
Assign
 ├── Var(x)
 └── BinOp(+)
     ├── Var(x)
     └── Num(1)
```

---

### 3️⃣ Abstract Syntax Tree (AST)

The AST represents the **structure** of the program, not its execution.

Key AST nodes:

* Program
* Block
* Assign
* Var
* Num
* BinOp
* If
* While

---

### 4️⃣ Interpreter

The interpreter walks the AST and executes it:

* Maintains a symbol table (`env`)
* Evaluates expressions
* Executes control flow (`if`, `while`)

This is implemented using the **visitor pattern**.

---

## ▶️ How to Run

### Requirements

* Python 3.10+

### Run

```bash
python tinycpp.py
```

Expected output:

```python
{'x': 5}
```

---

## 🚧 Current Limitations

* `for` loop is parsed but not executed
* Single global scope (no block-level scoping)
* No `print()` statement inside the language
* No functions or return statements

These limitations are intentional to keep the interpreter simple.

---

## 🛣 Planned Extensions

* Full `for` loop execution
* `print(x);` statement
* Block-level variable scoping
* Functions and return values
* Reading source code from `.cpp`-like files

---

## 🎓 Educational Purpose

This project is ideal for learning:

* How C++-style languages are parsed
* How AST-based interpreters work
* Recursive-descent parsing techniques
* Visitor pattern in interpreters

````
