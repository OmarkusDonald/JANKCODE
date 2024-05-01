from lexer import Lexer
from mathparser import Parser
from interpreter import Interpreter
from values import Number, Variable, Boolean


import re

class functionParser:
    def __init__(self):
        self.lines = []
        self.currentLine = 0
        self.variables = {}

    #not completely implemented 
    def _varmap(self, targetVar):
        for variable, value in self.variables.items():
            if targetVar == variable: return value

        print("Variable '" + str(targetVar) + "' is not found, line '" + str(self.currentLine) + "'")
    
    #the function scope(main) is sent here first 
    def parse(self, input):
        self.lines = input.splitlines()

        index = 0
        line = self.lines[0]

        for curIndex, curline in enumerate(self.lines):
            if curIndex == index and curline == line:
                self.currentLine += 1
                index = self.currentLine
                
                if line != "":
                    self._parseCommand(line.strip())       #use to be just line
                
            if index != self.currentLine:
                index = self.currentLine
            if index <= len(self.lines) -1:
                    line = self.lines[index]

    
    def _parseCommand(self, line):
        regex = re.search('^ *(?P<cmd>System.out.println|cout *<<|[Ss]tring|int|bool|boolean|if|while|for|[a-zA-Z][\w]*\+\+|}) *(?P<arg>.*)', line)

        if regex == None:
            return print("Failed to parse line '" + str(self.currentLine) + "' check syntax rules.")
        #else:
        #    print(self.currentLine)                #simply for visualization not needed let's me know the line number and line
        #    print(line.strip())                 

        if "++" in regex.group("cmd"):
            self._commandIncrement(line.strip())
        else:
            #matching sending the line to whatever command it matches. ALSO Python doesn't allow fall thru like in switch cases
            match regex.group("cmd").strip():
                case 'System.out.println' | 'cout <<'|'cout<<':
                    self._commandPrint(line.strip())
                case 'string' | 'String' | 'int' | 'bool' | 'boolean':
                    self._commandAssign(line.strip())
                case 'if':
                    self._commandIf(line.strip())
                case 'while':
                    self._commandWhile(line.strip())
                case 'for':
                    self._commandFor(line.strip())
                case '}':
                    self._commandClosingBrace(line.strip())
                case default:
                    return print("Failed to parse command on line '" + str(self.currentLine) + "'") 

    #THIS as far as I checked is working the variables and values are being stored in self.variables. NOTe boolean/bool are need really bool rather string and ints get converted to floats by the lexer etc        
    def _commandAssign(self, line):
        regex = re.search("^(?P<ASSIGN>string|String|int|bool|boolean)( *)(?P<var>[a-zA-Z][\w]*)( *)=( *)(?P<eval>.*);", line)

        if regex == None:
            return print("Assignment command syntax is invalid, line '" + str(self.currentLine) + "'")
        
        match regex.group("ASSIGN"):
            case 'string' | 'String':
                var = regex.group("var").strip()
                eval = regex.group("eval").strip()
                val = eval.strip('\"')                          #removing quotation marks from start and end

                self.variables.update({var:val})  
            
            case 'int':
                var = regex.group("var").strip()
                eval = regex.group("eval").strip()

                lexer = Lexer(eval.strip(), self.variables)
                tokens = lexer.generate_tokens()
                parser = Parser(tokens)
                tree = parser.parse()
                #if not tree:
                #    continue
                interpreter = Interpreter()
                val = interpreter.visit(tree).value
                self.variables.update({var:val})

            case 'bool' | 'boolean':                                        #assuming the user put either True or False
                var = regex.group("var").strip()
                eval = regex.group("eval").strip()

                self.variables.update({var:val})                #Convert the string to bool so we don't need to do it later
    

    #currently being worked on 
    def _commandPrint(self, line):
        cregex1 = re.search("^(?P<cppPrint>cout *<<)(?P<arg>.*);", line)                                #C++ Regex for print
        jregex2 = re.search("(?P<javaPrint>System.out.println)\( *(?P<arg>.*?) *\);", line)             #Java Regex for print

        String = None           
        Variable = None         


        if cregex1 == None and jregex2 == None:                                                                 #checking what regex was a match
            return print("print command syntax is invalid, line '" + str(self.currentLine) + "'") 
        
        elif cregex1 != None:
            Arg = cregex1.group('arg').strip()
            if re.search("\"(?P<str>.*)\"", Arg) !=None: String = re.search("\"(?P<str>.*)\"", Arg).group('str')                                                #if a string pattern is found
            if re.search("^ *(?P<variable>[a-zA-Z][\w]*)", Arg) !=None: Variable = re.search("^ *(?P<variable>[a-zA-Z][\w]*)", Arg).group('variable')           #variable pattern is found

        elif jregex2 != None:
            Arg = jregex2.group('arg').strip()
            if re.search("\"(?P<str>.*)\"", Arg) !=None: String = re.search("\"(?P<str>.*)\"", Arg).group('str')
            if re.search("^ *(?P<variable>[a-zA-Z][\w]*)", Arg) !=None: Variable = re.search("^ *(?P<variable>[a-zA-Z][\w]*)", Arg).group('variable')


        if String != None:
            print(String)
        elif Variable != None:
            if self._varmap(Variable) !=None:
                print(str(self._varmap(Variable)))               #prints out variable = value REMEMBER NUMBERS DISPLAYED AS FLOATS
        else:
            print("EVIL ERROR look at end of command Print no string or Variable")

    def _commandWhile(self, currentLine):
        cregex = re.search("^ *while[\s]*\((?P<condition>.+)\)[\s]*", currentLine)

        condition = cregex.group("condition").strip()

        lexer = Lexer(condition, self.variables)
        tokens = lexer.generate_tokens()
        parser = Parser(tokens)
        tree = parser.parse()
        #if not tree:
        #    continue
        interpreter = Interpreter()
        conditionBool = True

        if not bool(interpreter.visit(tree).value):
            conditionBool = False

        #store lines from current line to last line
        nextLines = []

        #iterates thru the future lines after while command line
        for line in range(self.currentLine, len(self.lines)):
            lineAdd = self.lines[line]
            nextLines.append(lineAdd)

        braceCounter = 0
        linesSkipped = 0
        whileScopeLines = []

        for line in nextLines:
            if braceCounter == -1:
                break
            else:
                for char in line:
                    if char == "{":
                        braceCounter += 1
                    elif char == "}":
                        braceCounter -= 1

            linesSkipped += 1
            whileScopeLines.append(line)

        while conditionBool:
            for line in whileScopeLines:
            
                if line != "":
                    self._parseCommand(line.strip())
            
            lexer = Lexer(condition, self.variables)
            tokens = lexer.generate_tokens()
            parser = Parser(tokens)
            tree = parser.parse()
            #if not tree:
            #    continue
            interpreter = Interpreter()
            conditionBool = True

            if not bool(interpreter.visit(tree).value):
                conditionBool = False

        self.currentLine += linesSkipped
        
        

    def _commandIf(self, currentLine):
        regex = re.search('(?P<if>if|else if) *\((?P<condition>[^()].*)\) *{', currentLine.strip())

        unParsedCond = regex.group("condition")

        
        regCond = re.search('(?P<cond1>[a-zA-Z0-9>=<! ]*[^|&])? *(?P<andOr>&&|\|\|)?(?P<rest>.*)', unParsedCond)

        #stores all conditions
        condQueue = []

        #store lines from current line to last line
        nextLines = []

        braceCounter = 0
        linesSkipped = 0
        ifScopeLines = []

        for line in range(self.currentLine, len(self.lines)):
                lineAdd = self.lines[line]
                nextLines.append(lineAdd)

        

        for index, line in enumerate(nextLines):
            if braceCounter == -1:
                break
            else:
                for char in line:
                    if char == "{":
                        braceCounter += 1
                    elif char == "}":
                        braceCounter -= 1

                #if braceCounter == -1:
                 #   if "else if" in line or "else" in line:
                  #      elseIf_elseStatement = True
                   # else: 
                    #    tempLine = nextLines[index + 1]
                
                    #while tempLine != None:
                    #    if tempLine.isspace():
                    #        tempLine = nextLines[index + 1]
                    #   elif "else if" in tempLine or "else" in tempLine:
                    #       elseIf_elseStatement = True
                    #       tempLine = None
                    #   else:
                    #       elseIf_elseStatement = False
                    #       tempLine = None

                linesSkipped += 1
                ifScopeLines.append(line)

        #eval call conds store them in order in a list
        while regCond != None:

            lexer = Lexer(regCond.group("cond1"), self.variables)
            tokens = lexer.generate_tokens()
            parser = Parser(tokens)
            tree = parser.parse()
            if not tree:
                return False  # Return False if there's no tree
            interpreter = Interpreter()
            value = interpreter.visit(tree)
            condQueue.append(bool(value.value))

            if regCond.group("andOr") != None:
                condQueue.append(regCond.group("andOr"))
                unParsedCond = regCond.group("rest")

             
            if unParsedCond != regCond.group("cond1"): 
                regCond = re.search('(?P<cond1>[a-zA-Z0-9>=<! ]*[^|&])? *(?P<andOr>&&|\|\|)?(?P<rest>.*)', unParsedCond)
            else:
                if regCond.group("andOr") == None:
                    lexer = Lexer(regCond.group("cond1"), self.variables)
                    tokens = lexer.generate_tokens()
                    parser = Parser(tokens)
                    tree = parser.parse()
                    if not tree:
                        return False  # Return False if there's no tree
                    interpreter = Interpreter()
                    value = interpreter.visit(tree)
                    condQueue.append(bool(value.value))
                break

        condQueue.pop()
        x = condQueue.pop(0)

        #Logic for multiple conditions
        while len(condQueue) != 0:
            
            if len(condQueue) != 0:
                y = condQueue.pop(0)
                if len(condQueue) != 0:
                    z = condQueue.pop(0)
                else:
                    print("Not correct amount of conditions")

            if x == True:
                if "&&" in y:
                    if z == False:
                        x = False
            elif x == True and "||" in y:
                continue

        #BELOW CODE IS LOGIC ABOVE IS LOGIC FOR CONDITIONS

        if x == True:        
            

            for line in ifScopeLines:        
                if line != "":
                    self._parseCommand(line.strip())
            
            self.currentLine += linesSkipped

        elif x == False:
            self.currentLine += linesSkipped

        #ADD A WAY TO SKIP OTHER ELIF OR ELSE IF ONE IS TRUE AND A WAY TO SKIP FALSE IF STATEMENTS UNTIL EITHER A TRUE, ELSE, OR NEITHER IS REACHED.

    

    
    def _commandAssignNewVal(self, currentLine):
        regex = re.search('^(?P<varName>[a-zA-Z][\w]*) *= (?P<expression>*.*);$', currentLine.strip())

        varName = regex.group("varName")
        expression = regex.group("expression")

        regexExpressionVar = re.search("[a-zA-Z][\w]*",expression.strip())
        regexExpressionNum = re.search("[0-9]+\.[0-9]+|[0-9]+",expression.strip())

        if regexExpressionVar != None:
            self.variables[varName] = self._varmap(expression)
        elif regexExpressionNum != None:
            self.variables[varName] = expression
        else:
            print("What the flip? Malformed expression")



    def _commandIncrement(self, currentLine):
        regex = re.search('^(?P<varName>[a-zA-Z][\w]*)\+\+;$', currentLine.strip())

        if regex != None:
            varName = regex.group("varName")
            tempStorage = self._varmap(varName)
            self.variables[varName] = float(tempStorage) + 1
        else:
            print("Increment aint working man")

    def _commandClosingBrace(self, currentLine):
        return
      