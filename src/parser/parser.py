

'''

"A | B"
"A ^ B"
"->"
"<->"
"<-"
"!"
'''



from sympy import sympify
from sympy.logic.boolalg import to_cnf
from src.dto.models import Clause, Expression, Literal
import re
from src.dto.models import Literal, Expression, Clause, Agent, Operator



# Define the string representation of the logical expression
# (not(A) | not(C)) & (not(B) | C ) -> not(A)
# Convert the string to a SymPy expression


from typing import Dict, List
from itertools import product

class Literal:
    """
    Represents a literal.
    :param
    - `is_not`: boolean.
    - `literal`: str.
    """
    def __init__(self, is_not: bool = False, literal: str = ''):
        self.is_not = is_not
        self.literal = literal

class Expression:
    def __init__(self, literals: List[Literal]):
        self.literals = literals

class Clause:
    def __init__(self, expressions: List[Expression]):
        self.expressions = expressions

class Agent:
    def __init__(self, beliefs: List[Clause]):
        self.beliefs = beliefs

def extract_variables(agent: Agent) -> List[str]:
    variables = set()
    for clause in agent.beliefs:
        for expression in clause.expressions:
            for literal in expression.literals:
                variables.add(literal.literal)
    return list(variables)

def evaluate_expression(expression: Expression, truth_values: Dict[str, bool]) -> bool:
    result = False
    for literal in expression.literals:
        value = truth_values.get(literal.literal, False)
        if literal.is_not:
            value = not value
        result = result or value
    return result

def evaluate_agent(agent: Agent) -> List[bool]:
    variables = extract_variables(agent)
    truth_combinations = product([False, True], repeat=len(variables))
    results = []
    for combination in truth_combinations:
        truth_values = dict(zip(variables, combination))
        result = all(evaluate_expression(expression, truth_values) for clause in agent.beliefs for expression in clause.expressions)
        results.append(result)
    return results

# Example usage:
# Define your Agent instance
agent = Agent([
    Clause([
        Expression([Literal(literal="A")]),
        Expression([Literal(literal="B")])
    ]),
    Clause([
        Expression([Literal(literal="C", is_not=True)])
    ])
])

# Evaluate the agent
results = evaluate_agent(agent)
print("Results for all possible combinations of truth values:")
print(results)


def parse(logicaal_expression: str = None):
    expression = sympify(logicaal_expression, evaluate=False)

    # Convert the expression to CNF
    cnf_expression = to_cnf(expression)

    print("Original Expression:", expression)
    print("CNF Expression:", cnf_expression)

    # cnf-string --> CNF() object --> belief

    ###create_CNF(cnf_expression)

    return cnf_expression




class create_CNF:
    def __init__(self, cnf_string: str):
        # here we parse the CNF string and create the Clause objects

        split_text: list = re.split("&", str(cnf_string))
        split_text = [text.replace("(", "").replace(")", "").replace(" ", "") for text in split_text]
        clauses = []
        for clause in split_text:
            clauses.append(create_clause(clause).clause)
        self.cnf = Clause(clauses=clauses)

class create_clause:
    def __init__(self, string: str):
        expressions = []
        for expression in string.split("|"):
            expressions.append(create_expression(expression).expression)
        self.clause = Expression(expression=expressions)


class create_expression:
    def __init__(self, string: str):
        is_not = False
        print(string)
        if re.match("~", string):
            is_not = True
            string = string[1:]
        self.expression = Literal(is_not=is_not, literal=string)



# parse(expression_str)
