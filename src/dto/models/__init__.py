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


# A is a Literal but also !A
class Literal(BaseModel):
    """
    Represents a literal.
    :param
    - `is_not`: boolean.
    - `literal`: str.
    """
    is_not: bool = False
    literal: str


class Expression(BaseModel):
    # should have the form (S1 OR S2 OR ... OR SN)
    expression: List[Literal]


class Clause(BaseModel):
    # clause with (AND) in between
    clauses: List[Expression]


class Agent(BaseModel):
    beliefs: List[CNF] # def. list of expressions

