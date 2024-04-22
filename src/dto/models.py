from typing import List

import sympy
from pydantic import BaseModel
from enum import Enum
from sympy import sympify
from sympy.logic.boolalg import to_cnf



class Operator(Enum):
    NOT = "!"
    AND = "&"
    OR = "OR"

# A is a an expressions but also !A
class Expression(BaseModel):
    is_not: bool = False
    expression: str

class Clause(BaseModel):
    # should have the form (S1 OR S2 OR ... OR SN)
    expressions: List[Expression]

class CNF(BaseModel):
    # clause with (AND) in between
    clauses: List[Clause]


class Agent(BaseModel):
    beliefs: List[CNF] # def. list of expressions

