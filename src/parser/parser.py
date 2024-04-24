

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
from src.dto.models import CNF, Clause, Expression
import re
from src.dto.models import Expression, Clause, CNF, Agent, Operator



# Define the string representation of the logical expression
# (not(A) | not(C)) & (not(B) | C ) -> not(A)
# Convert the string to a SymPy expression



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
        self.cnf = CNF(clauses=clauses)
class create_clause:
    def __init__(self, string: str):
        expressions = []
        for expression in string.split("|"):
            expressions.append(create_expression(expression).expression)
        self.clause = Clause(expressions=expressions)


class create_expression:
    def __init__(self, string: str):
        is_not = False
        print(string)
        if re.match("~", string):
            is_not = True
            string = string[1:]
        self.expression = Expression(is_not=is_not, expression=string)

# parse(expression_str)
