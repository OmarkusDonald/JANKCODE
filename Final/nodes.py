from dataclasses import dataclass

@dataclass
class NumberNode:  #number node that we want as float value
    value: float

    def __repr__(self):
        return f"{self.value}"
    
@dataclass
class VariableNode:   #I don't believe I use this node anymore check before done
    name: str                   
    def __repr__(self):         
        return f"{self.name}"    

@dataclass
class AddNode:   #addition represent by adding node a and b
    node_a: any
    node_b: any

    def __repr__(self):
        return f"({self.node_a}+{self.node_b})"

#Logic is basically the same but use the respective symbol    
@dataclass
class SubNode:
    node_a: any
    node_b: any

    def __repr__(self):
        return f"({self.node_a}-{self.node_b})"
    
@dataclass
class MultiNode:
    node_a: any
    node_b: any

    def __repr__(self):
        return f"({self.node_a}*{self.node_b})"

@dataclass
class DivNode:
    node_a: any
    node_b: any

    def __repr__(self):
        return f"({self.node_a}/{self.node_b})"
    
@dataclass
class RemainNode:
    node_a: any
    node_b: any

    def __repr__(self):
        return f"({self.node_a}%{self.node_b})"

@dataclass
class ExponNode:
    node_a: any
    node_b: any

    def __repr__(self):
        return f"({self.node_a}**{self.node_b})"

#positive number node    
@dataclass
class PositiveNode:
    node: any

    def __repr__(self):
        return f"(+{self.node})"
    
#negative number node
@dataclass
class NegativeNode:
    node: any

    def __repr__(self):
        return f"(-{self.node})"
    
#NEW
#BELOW
    
@dataclass
class EqualNode:
    node_a: any
    node_b: any

    def __repr__(self):
        return f"({self.node_a}={self.node_b})"
    
@dataclass
class EqualToNode:
    node_a: any
    node_b: any

    def __repr__(self):
        return f"({self.node_a}=={self.node_b})"
    
@dataclass
class NotEqualNode:
    node_a: any
    node_b: any

    def __repr__(self):
        return f"({self.node_a}!={self.node_b})"

@dataclass
class LessEqualNode:
    node_a: any
    node_b: any

    def __repr__(self):
        return f"({self.node_a}<={self.node_b})"
    
@dataclass
class GreatEqualNode:
    node_a: any
    node_b: any

    def __repr__(self):
        return f"({self.node_a}>={self.node_b})"
    
@dataclass
class LessThanNode:
    node_a: any
    node_b: any

    def __repr__(self):
        return f"({self.node_a}<{self.node_b})"
    
@dataclass
class GreatThanNode:
    node_a: any
    node_b: any

    def __repr__(self):
        return f"({self.node_a}>{self.node_b})"

@dataclass
class OrNode:
    node_a: any
    node_b: any

    def __repr__(self):
        return f"({self.node_a}OR{self.node_b})"

@dataclass
class AndNode:
    node_a: any
    node_b: any

    def __repr__(self):
        return f"({self.node_a}AND{self.node_b})"





