from tokens import Token, TokenTypes

WHITESPACE = ' \n\t'  #space newline and tab  
DIGITS = '0123456789'   #0-9
VARIABLES = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'  #not including uppercase for now

class Lexer:
    def __init__(self, text, varDict):         #CHANGED varDict = None to varDict
        self.text = iter(text)
        self.varDict = varDict                             
        self.advance()          #advance to first char

    #Move to next char and save it
    def advance(self):      
        try:
            self.current_char = next(self.text)
        except StopIteration:
            self.current_char = None        #end of the text

    #This method will generate all the possible tokens from the given text        
    def generate_tokens(self):
        #most of the of tokens operate similar besides for whitespace, numbers, and variables
        while self.current_char != None:
            if self.current_char in WHITESPACE:     #if it's a whitespace character(defined above) skip it
                self.advance()
            elif self.current_char == '.' or self.current_char in DIGITS:   #token for number working with floats so consider decimals 
                yield self.generate_number()
            # elif self.current_char in VARIABLES:    #if the current char is a variable use the handle_variable method         
            #     varName = self.current_char                 
            #     self.advance()                               
            #     yield self.handle_variable(varName)
            elif self.current_char == '+':
                self.advance()
                yield Token(TokenTypes.ADDITION)
            elif self.current_char == '-':
                self.advance()
                yield Token(TokenTypes.SUBTRACTION)
            elif self.current_char == '*':
                self.advance()
                yield Token(TokenTypes.MULTIPLICATION)
            elif self.current_char == '/':
                self.advance()
                yield Token(TokenTypes.DIVISION)
            elif self.current_char == '^':
                self.advance()
                yield Token(TokenTypes.EXPONENTIAL)
            elif self.current_char == '%':
                self.advance()
                yield Token(TokenTypes.PERCENTAGE)
            elif self.current_char == '(':
                self.advance()
                yield Token(TokenTypes.LEFTPAREN)
            elif self.current_char == ')':
                self.advance()
                yield Token(TokenTypes.RIGHTPAREN)
            elif self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    yield Token(TokenTypes.EQUALS_TO)
                else:
                    yield Token(TokenTypes.EQUAL)
            elif self.current_char == '<':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    yield Token(TokenTypes.LESS_EQUAL)
                else:
                    yield Token(TokenTypes.LESS_THAN)
            elif self.current_char == '>':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    yield Token(TokenTypes.GREAT_EQUAL)
                else:
                    yield Token(TokenTypes.GREAT_THAN)
            elif self.current_char == '!':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    yield Token(TokenTypes.NOT_EQUALS)
                else:
                    raise Exception(f"Invalid syntax")
            elif self.current_char in VARIABLES:    #if the current char is a variable use the handle_variable method         
                varName = self.current_char                 
                self.advance()                               
                yield self.handle_variable(varName)
            else:
                raise Exception(f"Invalid character '{self.current_char}' ")    #whatever char entered is not valid
            

    def check_keyword(self, keyword):
        for char in keyword[1:]:
            if self.current_char != char:
                return False
            self.advance()
        return True
    
    def generate_number(self):     #forms the current number
        decimal_point_count = 0     #keeps track of how many decimals used
        number_str = self.current_char  #putting digits and decimals into number string to form a number
        self.advance()

        while self.current_char != None and (self.current_char == '.' or self.current_char in DIGITS):  
            if self.current_char == '.':    #check to for decimal and break if when more than 1 are found
                decimal_point_count += 1
                if decimal_point_count > 1:
                    break

            number_str += self.current_char #add current char to string
            self.advance()

        #if a number starts with a decimal we know the first number should be a zero .31 = 0.31
        if number_str.startswith('.'):      
            number_str = '0' + number_str

        #put a zero after the last char if it's a decimal
        if number_str.endswith('.'):
            number_str += '0'

        return Token(TokenTypes.NUMBER, float(number_str))  #we need to return not only the string in float form but the token type
    
    def handle_variable(self, varName):                                         #made to hadle variable inputs
        #check to see if it is in the dictionary 
        if self.varDict is not None and varName in self.varDict:
            return Token(TokenTypes.NUMBER, self.varDict[varName])
        
        #print an error letting the user know the value of the variable is not found
        else:
            print(f"Error: Val not found '{varName}'")