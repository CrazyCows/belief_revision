from sympy.logic import boolalg

from src.dto.models import Operator, Literal, Expression, Clause, Agent
from src.parser.parser import parse
import re

import pandas as pd
import sympy as sp

"""
def truth_table(expr_str):
    # Parse the expression using sympy
    expr = sp.sympify(expr_str)

    # Find all symbols in the expression
    symbols = sorted(expr.atoms(sp.Symbol), key=lambda s: s.name)

    # Generate all possible combinations of truth values
    rows = []
    for combo in range(2 ** len(symbols)):
        # Create a dictionary of truth values for this combination
        val_dict = {s: bool(combo & (1 << i)) for i, s in enumerate(symbols)}

        # Evaluate the expression with these truth values
        result = expr.subs(val_dict)

        # Add the row to the list
        rows.append({str(s): val_dict[s] for s in symbols} | {'result': bool(result)})

    # Create a DataFrame from the rows
    return rows
"""
def truth_table(expr_str):
    # Extract unique symbols from the expression
    symbols = sorted(set(char for char in expr_str if char.isalpha()))
    #print("--------")
    #print(symbols)
    {"name_key": "name_value"}
    # Generate all possible combinations of truth values for symbols
    rows = []
    for i in range(2 ** len(symbols)):
        # Finds all combination of boolean values, see example below:
        # A = 000, B = 010, C = 100, because of (1 << j)
        # i = 000 = 0
        # A = false, B = false, C = false
        # i = 001 = 1
        # A = True, B = false, C = false
        # i = 010 = 2
        # A = false, B = true, C = false
        # i = 011 = 3
        # A = true, B = true, C = false
        # i=100 = 4
        # A= false, b = false, C = true
        # i=101 = 5
        # A = true, b = false, C = true
        # i = 110 = 6
        # A = false, b = true, C = true
        # i = 111 = 7
        # A = true, b = true, c = true
        val_dict = {symbols[j]: bool(i & (1 << j)) for j in range(len(symbols))}
        result = eval(expr_str, {}, val_dict)

        rows.append({**val_dict, 'result': result})
    print(pd.DataFrame(rows))
    return rows

#Example usage:
#expression = 'A & (B | ~C)'  # Using '&' for AND, '|' for OR, '~' for NOT
#table = truth_table(expression)
#print(table)

if __name__ == "__main__":
    expression_str = '((~a | ~c) & (~b | c) >> ~a)'

    expressions = [
        "(~a | ~c) & (~b | c) >> ~a",
        "(a & b) | (~c & d) >> (b | ~d)",
        "(~a & b) | (c >> ~d)",
        "(a >> b) & (~c | d)",
        "(~a & ~b) | (~c & ~d)",
        "(a | b) & (c >> ~d) >> (~a | c)",
        "(a & ~b) >> (~c | d)",
        "(a >> ~b) & (c | ~d)",
        "(a | b) & c & ~d >> e",
        "(~a & b) | (c >> d & ~e)",
        "(a & b & c) | (~d & e)",
        "(a | ~b) & (c | d) >> (~e & a)",
        "(~a >> b) & (c & ~d)",
        "(a & b) | ~(c | d | e)",
        "(a >> ~b) & (~c >> d)",
        "(a | b | c) & (~d >> e)",
        "(~a & ~b) | (c & ~d & e)",
        "(a & ~b & ~c) >> (d | ~e)",
        "(a | b) & (~c & d & ~e)",
        "(~a >> b) & (c | d | ~e)",
        "(a & b) | (c & ~d) & e",
        "(a | ~b) & (c >> d) & ~e",
        "(a & b & c) | (~d | e)",
        "(a >> ~b) & (~c | d | e)",
        "(~a | b) & (c & ~d >> e)",
        "(a & b) & (~c >> d | e)",
        "(~a & ~b) | (c | ~d & e)",
        "(a | b | ~c) >> (d & e)",
        "(~a & b & c) | (d & ~e)",
        "(a | ~b & c) & (d >> ~e)"
    ]

    expressions2 = [
        "(p)",
        "(q)",
        "(~p | r)",
        "(s)",
        "(u | v)",
        "(~s | ~r)",
        "(~t & p)",
        "(t)"
    ]

    # print(cnf_form)

    beliefs = []
    beliefs_tmp = []

    def check_for_truth(table_is):
        """
        Function that checks for if a statement is a contradiction
        :param table_is: the truth table
        :return: returns True if a statement can be true and false if it is a contradiction
        """
        for row in table_is:
            if row['result'] is True or row['result'] == 1:
                return True
        print("IM FALSE MAN")
        return False

    def contraction(beliefs):
        beliefs_string = " ) & ( ".join(beliefs)
        beliefs_string = "( " + beliefs_string + " )"

        #print(beliefs_string)

        table_is = (truth_table(beliefs_string))

        #print(pd.DataFrame(table_is))


        if check_for_truth(table_is):
            pass
        else:
            iterate_to = len(beliefs)
            for i, belief in enumerate(reversed(beliefs), 1):



                beliefs_tmp = beliefs.copy()
                beliefs_tmp.pop(i)

                beliefs_temp_string = " ) & ( ".join(beliefs_tmp)
                beliefs_temp_string = "( " + beliefs_temp_string + " )"

                table = truth_table(beliefs_temp_string)
                is_true = check_for_truth(table)
                # B
                # (A or C) -> A
                # not(A)

                # A
                # not(A) ->

                if is_true:
                    beliefs.pop(i)
                    print("IM TRUE MAN")
                    break



        # TODO: Implement removal of thingies
        print(beliefs)

    stop_counter = 0
    for expression in expressions2:


        cnf_form = parse(expression)
        cnf_form = str(cnf_form)
        print(cnf_form)
        beliefs.append(cnf_form)



        amount = len(re.findall("&", cnf_form)) + 1
        if amount > 1:
            beliefs.pop()
            beliefs_tmp = beliefs.copy()
            for i in range(amount):
                newest_beliefs_OG = cnf_form.replace("(", "").replace(")", "")
                # Text string is 5
                newest_beliefs = newest_beliefs_OG.split(" & ")
                # This is range 20?
                beliefs_tmp.append(newest_beliefs[i])
                contraction(beliefs_tmp)
            beliefs.append(newest_beliefs_OG)
            print(beliefs)
        else:
            contraction(beliefs)








    #print(table_is[len(table_is)-1])



    belief_base = []
    clause = []
    expression = []
    #print(cnf_form.cnf.clauses[0].expression)












"""
(A | B ->  C)
 = not(A | B) | C
 = not(A) & not(B) | C 
 
 

A ^ B -> not(C)
 = not(A ^ B) | not(C)
 = not(A) | not(B) | not(C)
 
 K1
 
 K2
 
 
 
 1. req = (not(A) | not(C)) & not(B)
 2. req = A & B
 
 
 (b | ~a) & (~a | ~c)
 (not(A) | not(C)) & (not(B) | C ) -> not(A) 
 
 k1:
 a = 0 => c = 1|0
 a = 1 => c = 0
 
 k2:
 b = 0 => c = 0|1
 b = 1 => c = 1
 
 k1 & k2:
  a = 0 => c = 1|0 && b = 0 => c = 0|1
  a = 0 => c = 1|0 && b = 1 => c = 1
  a = 1 => c = 0 && b = 0 => c = 0|1
  a = 1 => c = 0 && b = 1 => c = 1
  
req 2: 
  a = 0 => b = 1|0 && c = 1|0
  a = 1 => b = 0 => c = 1|0
  b = 0 => c = 1|0 && c = 1|0
  
 
 if 
 2. req = A cannot do
 or 
 2. req = (A & B & C) no can do!
 
 A = 0
 B = 1 or 0
 C = not(b) if b != 1

Prio:
1. Do nothing
2. Contraction
3. Revision

points (?):


 Generally: 
 (K1 & K2 & ...  & KN
 
 
 
 left from req 1 = 
 
 
"""

"""
 1. BELIEFSET{{a},{b}, {AND(a,b) => c},  NOT(c)}
 if we now gat the new belief of NOT(c) then we can revise the set 
 of belief in the following of two ways: 
 
    - we remove the a will result in {AND(a,b) => NOT(c)} and NOT(c) being true
    - same if we remove b
    - if we remove the entire implecation {AND(a,b) => NOT(c)}
 
"""