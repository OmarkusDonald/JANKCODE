from enum import Enum
from dataclasses import dataclass

#All possible tokens for our program
class TokenTypes(Enum):     #associating names with id numbers ENUM
    NUMBER = 0              
    ADDITION = 1
    SUBTRACTION = 2
    MULTIPLICATION = 3
    DIVISION = 4
    EXPONENTIAL = 5
    PERCENTAGE = 6
    LEFTPAREN = 7
    RIGHTPAREN = 8
    VARIABLE = 9 
    EQUAL = 10
    EQUALS_TO = 11
    NOT_EQUALS = 12
    LESS_EQUAL = 13
    GREAT_EQUAL = 14
    LESS_THAN = 15
    GREAT_THAN = 16
    LOGICAL_AND = 17
    LOGICAL_OR = 18


@dataclass
class Token:
    type: TokenTypes    #token's type
    value: any = None   #token's value, some have None so default none

