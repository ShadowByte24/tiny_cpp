# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
INT, IF,ELSE,WHILE,FOR='INT','IF','ELSE','WHILE','FOR'
LPAREN,RPAREN,LBRACE,RBRACE,SEMI,ASSIGN='LPAREN','RPAREN','LBRACE','RBRACE','SEMI','ASSIGN'
PLUS,MINUS,MUL,DIV='PLUS','MINUS','MUL','DIV'
LT,GT,LE,GE,EQ,NE='LT','GT','LE','GE','EQ','NE'
ID,NUMBER='ID','NUMBER'
EOF='EOF'


class Token(object):
    def __init__(self,type,value):
        self.type=type #integer
        self.value=value    #'2'

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
        """
        return 'TOKEN({type},{value})'.format(
            type=self.type,
            value=repr(self.value)
            )
    
    def __repr__(self):
        return self.__str__()
    


RESERVED_KEYWORDS = {
    'int': Token(INT, 'int'),
    'if': Token(IF, 'if'),
    'else': Token(ELSE, 'else'),
    'while': Token(WHILE, 'while'),
    'for': Token(FOR, 'for'),
}


class lexer(object):
    def __init__(self,text):
        # client string if,else or loop
        self.text=text
        self.pos=0 #self.pos is index in self.text
        # current token instance
        self.current_token= None
        self.current_char=self.text[self.pos] 

    ############################################
                # L3x3r C0d3 #
    ############################################
    def error(self):
        raise Exception('Invalid syntax')
    
    def advance(self):
        #Advance the `pos` pointer and set the `current_char` variable.
        self.pos+=1
        if self.pos > len(self.text) -1:
            self.current_char=None # indicates end of input
        else:
            self.current_char=self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    def int(self):
        # return a multidigit integer
        result=''
        while self.current_char is not None and self.current_char.isdigit():
            result+=self.current_char
            self.advance()
        return result
    
    def _id(self):
        """Handle identifiers and keywords"""
        result=''
        while self.current_char is not None and self.current_char.isalnum():
            result+=self.current_char
            self.advance()

        token=RESERVED_KEYWORDS.get(result,Token(ID,result))
        return token
    
    def peek(self):
        peek_pos=self.pos+1
        if peek_pos>len(self.text)-1:
            return None
        else:
            return self.text[peek_pos]
        

    
    def get_next_token(self):
        """Lexical Analyzer(aka scanner or tokenizer)
        This method is responsible for breaking sentence into token 
        apart into tokens. One toke at a time"""
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isalpha():
                return self._id()
            
            if self.current_char.isdigit():
                return Token(NUMBER,self.int())
            
            if self.current_char =='+':
                self.advance()
                return Token(PLUS,'+')
            
            if self.current_char =='-':
                self.advance()
                return Token(MINUS,'-')
            
            if self.current_char =='*':
                self.advance()
                return Token(MUL,'*')
            
            if self.current_char =='/':
                self.advance()
                return Token(DIV,'/')
            
            if self.current_char =='>' and self.peek()=='=':
                self.advance()
                self.advance()
                return Token(GE,'>=')
            
            if self.current_char =='<' and self.peek()=='=':
                self.advance()
                self.advance()
                return Token(LE,'<=')
            
            if self.current_char =='=' and self.peek()=='=':
                self.advance()
                self.advance()
                return Token(EQ,'==')
            
            if self.current_char =='!' and self.peek()=='=':
                self.advance()
                self.advance()
                return Token(NE,'!=')
            
            if self.current_char =='>':
                self.advance()
                return Token(GT,'>')
            
            if self.current_char =='<':
                self.advance()
                return Token(LT,'<')
            
            if self.current_char =='=':
                self.advance()
                return Token(ASSIGN,'=')
            
            if self.current_char ==';':
                self.advance()
                return Token(SEMI,';')
            
            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            if self.current_char == '{':
                self.advance()
                return Token(LBRACE, '{')

            if self.current_char == '}':
                self.advance()
                return Token(RBRACE, '}')

                        
            self.error()
        return Token(EOF,None)
    

######### AST Nodes ##########
class AST:
    pass

class Program(AST):
    def __init__(self,statements):
        self.statements=statements
    
class Block(AST):
    def __init__(self,statements):
        self.statements=statements
        
class Assign(AST):
    def __init__(self,name,expr):
        self.name=name
        self.expr=expr

class Var(AST):
    def __init__(self,name):
        self.name=name

class Num(AST):
    def __init__(self, value):
        self.value = value

class BinOp(AST):
    def __init__(self,left,op,right):
        self.left=left
        self.op=op
        self.right=right

class If(AST):
    def __init__(self,cond,then_block,else_block=None):
        self.cond=cond
        self.then_block=then_block
        self.else_block=else_block
        
class While(AST):
    def __init__(self,cond,body):
        self.cond=cond
        self.body=body


class Parser(object):

    ##########################################################
    # Parser / Interpreter code                              #
    ##########################################################

    def __init__(self,lexer):
        self.lexer=lexer
        #set current token to the first token taken from the input
        self.current_token=self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self,token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # o/w raise an exception
        if self.current_token.type==token_type:
            self.current_token=self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        """ factor → NUMBER | IDENT | "(" expr ")" """
        token=self.current_token

        if token.type==NUMBER:
            self.eat(NUMBER)
            return Num(int(token.value))
         
        elif token.type==ID:
            name=token.value
            self.eat(ID)
            return Var(name)

        elif token.type==LPAREN:
            self.eat(LPAREN)
            result=self.expr()
            self.eat(RPAREN)
            return result
        
        else:
            self.error()
        
    def term(self):
        """  factor (( "*" | "/" ) factor)*  """
        node=self.factor()

        while self.current_token.type in (MUL,DIV):
            token=self.current_token
            if token.type==MUL:
                self.eat(MUL)
            else:
                self.eat(DIV)
            node=BinOp(node,token.type,self.factor())
        return node

        
    def arithmetic_expr(self):
        """ term (( "+" | "-" ) term)* """
        node=self.term()
        while self.current_token.type in (PLUS,MINUS):
            token=self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            else:
                self.eat(MINUS)

            node=BinOp(node,token.type,self.term())

        return node

    def comparison_expr(self):
        """  arithmetic_expr (( "<" | ">" | "<=" | ">=" ) arithmetic_expr)?   """
        node = self.arithmetic_expr()

        while self.current_token.type in (GT,LT,GE,LE):
            token=self.current_token
            self.eat(token.type)
            node=BinOp(node,token.type,self.arithmetic_expr())

        return node
    
    def equality_expr(self):
        """ comparison_expr (( "==" | "!=" ) comparison_expr)? """
        node=self.comparison_expr()
        while self.current_token.type in (EQ,NE):
            token=self.current_token

            if token.type == EQ:
                self.eat(EQ)

            elif token.type==NE:
                self.eat(NE)
            node=BinOp(node,token.type,self.comparison_expr())

        return node
  
    def expr(self):
        """" expr → equality_expr """
        return self.equality_expr()
    
    def while_statement(self):
        """ "while" "(" expr ")" block """
        self.eat(WHILE)
        self.eat(LPAREN)
        cond=self.expr()
        self.eat(RPAREN)
        body=self.block()
        return While(cond,body)

    def assignment(self):
        """ IDENT "=" expr  """
        name = self.current_token.value
        self.eat(ID)
        self.eat(ASSIGN)
        expr = self.expr()
        return Assign(name,expr)

    def declaration(self):
        """ "int" IDENT ";"  """
        self.eat(INT)
        self.eat(ID)
        self.eat(SEMI)


    def for_statement(self):
        """ "for" "(" assignment ";" expr ";" assignment ")" block  """
        self.eat(FOR)
        self.eat(LPAREN)

        self.assignment()
        self.eat(SEMI)

        self.expr()
        self.eat(SEMI)

        self.assignment()
        self.eat(RPAREN)
        self.block()
        return None

    def if_statement(self):
        """  "if" "(" expr ")" block
      ("else" "if" "(" expr ")" block)*
      ("else" block)? """
        self.eat(IF)
        self.eat(LPAREN)
        cond=self.expr()
        self.eat(RPAREN)
        then_block=self.block()

        else_block=None
        if self.current_token.type==ELSE:
            self.eat(ELSE)
            else_block=self.block()

        return If(cond,then_block,else_block)

            

    def block(self):
        self.eat(LBRACE)
        statements=[]
        while self.current_token.type!=RBRACE:
            stmt=self.statement()
            if stmt is not None:
                statements.append(stmt)
        self.eat(RBRACE)
        return Block(statements)
    
    def statement(self):
        """ declaration
        | assignment ";"
        | if_statement
        | while_statement
        | for_statement
        | block
        | empty """
        if self.current_token.type==INT:
            self.declaration()
            return None
        
        elif self.current_token.type==ID:
            node=self.assignment()
            self.eat(SEMI)
            return node
        
        elif self.current_token.type==IF:
            return self.if_statement()
        
        elif self.current_token.type==WHILE:
            return self.while_statement()
        
        elif self.current_token.type==FOR:
            return self.for_statement()
        
        elif self.current_token.type == SEMI:
            self.eat(SEMI)
            return None

        elif self.current_token.type==LBRACE:
            return self.block()
        
        else:
            # empty(e)
            self.error()


    def program(self):
        """  program → statement*  """
        statements=[]
        while self.current_token.type!=EOF:
            stmt=self.statement()
            if stmt is not None:
                statements.append(stmt)
        return Program(statements)
        

class Interpreter:
    def __init__(self):
        self.env={}

    def visit(self,node):
        method_name='visit_'+type(node).__name__
        visitor=getattr(self,method_name,self.no_visit)
        return visitor(node)
    
    def no_visit(self,node):
        raise Exception(f"No visit_{type(node).__name__} method")
    
    def visit_Program(self,node):
        for stmt in node.statements:
            self.visit(stmt)

    def visit_Block(self,node):
        for stmt in node.statements:
            self.visit(stmt)

    def visit_Num(self,node):
        return node.value
    
    def visit_Var(self,node):
        if node.name not in self.env:
            raise Exception(f"Undefined variable '{node.name}")
        return self.env[node.name]
    
    def visit_Assign(self,node):
        value=self.visit(node.expr)
        self.env[node.name]=value

    def visit_BinOp(self,node):
        left=self.visit(node.left)
        right=self.visit(node.right)

        if node.op == PLUS:
            return left+right
        
        if node.op == MINUS:
            return left-right
        
        if node.op == MUL:
            return left*right
        
        if node.op == DIV:
            return left//right
        
        if node.op == LT:
            return left<right
        
        if node.op == GT:
            return left>right
        
        if node.op == LE:
            return left<=right
        
        if node.op == GE:
            return left>=right
        
        if node.op == EQ:
            return left==right
        
        if node.op == NE:
            return left!=right
        
        raise Exception("Unknown operator")
    

    def visit_If(self,node):
        condition=self.visit(node.cond)

        if condition:
            self.visit(node.then_block)
        elif node.else_block:
            self.visit(node.else_block)

    def visit_While(self,node):
        while self.visit(node.cond):
            self.visit(node.body)

if __name__ == "__main__":
    source = """
    int x;
    x = 0;
    while (x < 5) {
        x = x + 1;
    }
    """

    lex = lexer(source)
    parser = Parser(lex)
    tree = parser.program()

    interp = Interpreter()
    interp.visit(tree)

    print(interp.env)
