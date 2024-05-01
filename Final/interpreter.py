from nodes import *
from values import Number, Variable, Boolean

class Interpreter:
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'    #visit_AddNode etc
        method = getattr(self, method_name)
        return method(node) 
    
    def visit_NumberNode(self, node):   #translate from number node to number type
        return Number(node.value)
    
    def visit_VariableNode(self, node): 
        varName = node.value
        if varName in self.varDict:
            return Variable(node.value)     
        else:
            raise ValueError(f"Variable '{varName}' has no value")
    
    def visit_PositiveNode(self, node):
        return self.visit(node.node)    #positive do nothing
    
    def visit_NegativeNode(self, node):
        return Number (-self.visit(node.node).value)    #turn negative
    
    #Logic is similar for most
    def visit_AddNode(self, node):  
        return Number(self.visit(node.node_a).value + self.visit(node.node_b).value)    #interpret left and right of add node, visit each node until signal number val to add together
    
    def visit_SubNode(self, node):
        return Number(self.visit(node.node_a).value - self.visit(node.node_b).value)
    
    def visit_MultiNode(self, node):
        return Number(self.visit(node.node_a).value * self.visit(node.node_b).value)
    
    def visit_DivNode(self, node):
        return Number(self.visit(node.node_a).value / self.visit(node.node_b).value)
    
    def visit_RemainNode(self, node):
        return Number(self.visit(node.node_a).value % self.visit(node.node_b).value)
    
    def visit_ExponNode(self, node):
        return Number(self.visit(node.node_a).value ** self.visit(node.node_b).value)
    

    #BELOW IS NEW ----------------------------------------------------------------------

    def visit_OrNode(self, node):
        return Boolean(self.visit(node.node_a).value or self.visit(node.node_b).value)

    def visit_AndNode(self, node):
        return Boolean(self.visit(node.node_a).value and self.visit(node.node_b).value)

    def visit_EqualNode(self, node):
        return Boolean(self.visit(node.node_a).value == self.visit(node.node_b).value)

    def visit_EqualToNode(self, node):
        return Boolean(self.visit(node.node_a).value == self.visit(node.node_b).value)

    def visit_NotEqualNode(self, node):
        return Boolean(self.visit(node.node_a).value != self.visit(node.node_b).value)

    def visit_LessEqualNode(self, node):
        return Boolean(self.visit(node.node_a).value <= self.visit(node.node_b).value)

    def visit_GreatEqualNode(self, node):
        return Boolean(self.visit(node.node_a).value >= self.visit(node.node_b).value)

    def visit_LessThanNode(self, node):
        return Boolean(self.visit(node.node_a).value < self.visit(node.node_b).value)

    def visit_GreatThanNode(self, node):
        return Boolean(self.visit(node.node_a).value > self.visit(node.node_b).value)