from dataclasses import dataclass
#different value types that the interpreter can produce

@dataclass
class Number:
    value: float    #value of number

    def __repr__(self):
        return f"{self.value}"      #string value of number


@dataclass
class Variable:
    value: str      

    def __repr__(self):
        return f"{self.value}"
 
    
def varMap(targetVariable, varDict):
    for var, val in varDict.items():
        if targetVariable == var:
            return val
    raise ValueError("Variable has no value")

@dataclass
class Boolean:
    value: bool

    def __repr__(self):
        return str(self.value)


    