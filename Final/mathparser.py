from tokens import TokenTypes
from nodes import *

#turn tokens into nodes
class Parser:
    #store tokens so we can access it easier
    def __init__(self, tokens):
        self.tokens = iter(tokens)
        self.advance()

    #error for improper syntax
    def raise_error(self):
        raise Exception("Invalid Syntax")

    #advance goes to next token until reaching the end
    def advance(self):
        try:
            self.current_token = next(self.tokens)
        except StopIteration:
            self.current_token = None
    
    
    def parse(self):
        #check to see if input is empty
        if self.current_token == None:
            return None
        
        #expr is the alpha method
        result = self.expr()

        #tokens left that did not get processed aka invalid syntax, sequences, etc
        if self.current_token != None:
            self.raise_error()

        return result
    
    def expr(self):
        result = self.compare_expr()

        while self.current_token != None and self.current_token.type in (TokenTypes.LOGICAL_OR, TokenTypes.LOGICAL_AND):
            if self.current_token.type == TokenTypes.LOGICAL_OR:
                self.advance()
                result = OrNode(result, self.compare_expr())
            elif self.current_token.type == TokenTypes.LOGICAL_AND:
                self.advance()
                result = AndNode(result, self.compare_expr())
        
        return result
      
    
    def compare_expr(self):
        result = self.addsub_expr()

        while self.current_token != None and self.current_token.type in (TokenTypes.EQUALS_TO, TokenTypes.NOT_EQUALS, TokenTypes.LESS_EQUAL, TokenTypes.GREAT_EQUAL,TokenTypes.GREAT_THAN, TokenTypes.LESS_THAN):
            if self.current_token.type == TokenTypes.EQUALS_TO:
                self.advance()
                result = EqualToNode(result, self.addsub_expr())
            elif self.current_token.type == TokenTypes.NOT_EQUALS:
                self.advance()
                result = NotEqualNode(result, self.addsub_expr())
            elif self.current_token.type == TokenTypes.LESS_EQUAL:
                self.advance()
                result = LessEqualNode(result, self.addsub_expr())
            elif self.current_token.type == TokenTypes.GREAT_EQUAL:
                self.advance()
                result = GreatEqualNode(result, self.addsub_expr())
            elif self.current_token.type == TokenTypes.LESS_THAN:
                self.advance()
                result = LessThanNode(result, self.addsub_expr())
            elif self.current_token.type == TokenTypes.GREAT_THAN:
                self.advance()
                result = GreatThanNode(result, self.addsub_expr())


        return result
    
    def addsub_expr(self):
        result = self.term()

        #checking for add and sub tokens make corresponding nodes
        while self.current_token != None and self.current_token.type in (TokenTypes.ADDITION, TokenTypes.SUBTRACTION):
            if self.current_token.type == TokenTypes.ADDITION:
                self.advance()
                result = AddNode(result, self.term()) 
            elif self.current_token.type == TokenTypes.SUBTRACTION:
                self.advance()
                result = SubNode(result, self.term())
            
        return result

    def term(self):
        result = self.power()  #changed to power

        while self.current_token != None and self.current_token.type in (TokenTypes.MULTIPLICATION, TokenTypes.DIVISION, TokenTypes.PERCENTAGE):
            if self.current_token.type == TokenTypes.MULTIPLICATION:
                self.advance()
                result = MultiNode(result, self.power())
            elif self.current_token.type == TokenTypes.DIVISION:
                self.advance()
                result = DivNode(result, self.power())
            elif self.current_token.type == TokenTypes.PERCENTAGE:
                self.advance()
                result = RemainNode(result, self.power())                       #CHANGED TO .power() use to be .factor() same for above
            
        return result
    
    def power(self):    #Makes exponents work
        result = self.factor()

        while self.current_token != None and self.current_token.type == (TokenTypes.EXPONENTIAL):
            if self.current_token.type == TokenTypes.EXPONENTIAL:
                self.advance()
                result = ExponNode(result, self.factor())
        return result
        
    
    def factor(self):
        token = self.current_token

        if token.type == TokenTypes.LEFTPAREN:
            self.advance()
            result = self.expr()

            #must be followed by right parentheses
            if self.current_token.type != TokenTypes.RIGHTPAREN:
                self.raise_error("Incorrect parentheses syntax")
            
            self.advance()
            return result
        
        elif token.type == TokenTypes.NUMBER:
            self.advance()
            return NumberNode(token.value)
        
        elif token.type == TokenTypes.VARIABLE:     #unused check before finished
            self.advance()                          
            return VariableNode(token.value)           

        elif token.type == TokenTypes.ADDITION:
            self.advance()
            return PositiveNode(self.factor())
        
        elif token.type == TokenTypes.SUBTRACTION:
            self.advance()
            return NegativeNode(self.factor())
          
        self.raise_error()