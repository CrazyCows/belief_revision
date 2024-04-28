import sys

from sympy.logic import boolalg

from src.dto.models import Operator, Literal, Expression, Clause, Agent
from src.parser.parser import parse
import re

import pandas as pd


def truth_table(expr_str):
    # Extract unique symbols from the expression
    symbols = sorted(set(char for char in expr_str if char.isalpha()))
    # print("--------")
    # print(symbols)
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
        # i = 100 = 4
        # A = false, b = false, C = true
        # i = 101 = 5
        # A = True, b = False, C = true
        # i = 110 = 6
        # A = false, b = true, C = true
        # i = 111 = 7
        # A = true, b = true, c = true
        val_dict = {symbols[j]: bool(i & (1 << j)) for j in range(len(symbols))}
        result = eval(expr_str, {}, val_dict)
        rows.append({**val_dict, 'result': result})
    # print(pd.DataFrame(rows))
    return rows


def check_for_truth(table_is):
    """
    Function that checks for if a statement is a contradiction
    :param table_is: the truth table
    :return: returns True if a statement can be true and false if it is a contradiction
    """
    for row in table_is:
        if row['result'] is True or row['result'] != 0:
            return True
    # print("IM FALSE MAN")
    return False


def check_correct_input(string):
    allowed_characters = set("ABCDEFGHIJKLMNOPQRSTUZ~&|>() ")
    alpha_count = 0
    for char in string:
        if char not in allowed_characters:
            return False
        if char.isalpha():
            alpha_count += 1
    if alpha_count == 0:
        return False
    return True


def contraction(local_beliefs, number_of_pops, belief_map, max_steps):
    if number_of_pops == max_steps:
        return []
    beliefs_string = " ) & ( ".join(local_beliefs)
    beliefs_string = "( " + beliefs_string + " )"

    # print(beliefs_string)

    table_is = (truth_table(beliefs_string))

    # print(pd.DataFrame(table_is))

    if check_for_truth(table_is):
        return local_beliefs
    else:
        temp_belief_list = []
        iterate_from = len(local_beliefs) - 2
        for i in range(iterate_from, -1, -1):
            beliefs_tmp = local_beliefs.copy()
            beliefs_tmp.pop(i)
            beliefs_tuple = tuple(beliefs_tmp)
            if beliefs_tuple in belief_map:
                return []
            temp_belief_list.append(beliefs_tmp.copy())

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
                local_beliefs.pop(i)
                belief_map[beliefs_tuple] = local_beliefs
                # print("IM TRUE MAN")
                return local_beliefs
            elif i == 0:
                best_belief = []
                k = 0
                if len(temp_belief_list) > 0:
                    for temp_belief in temp_belief_list:
                        print("depth: ")
                        print(number_of_pops)
                        print("beliefnr: ")
                        print(k)
                        k = k + 1
                        if isinstance(temp_belief, list):
                            temp_belief = contraction(temp_belief, number_of_pops + 1, belief_map, max_steps)
                        if (best_belief == [] or len(temp_belief) > len(best_belief)) and isinstance(temp_belief, list):
                            best_belief = temp_belief.copy()
                            max_steps = number_of_pops + 1
                    belief_map[beliefs_tuple] = best_belief
                    return best_belief
                else:
                    return []
    print(beliefs)


# Example usage:
# expression = 'A & (B | ~C)'  # Using '&' for AND, '|' for OR, '~' for NOT
# table = truth_table(expression)
# print(table)

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
        "(~p)"
    ]

    expressions3 = [
        "(C)",
        "(A)",
        "(B)",
        "(A & B)",
        "(D)",
        "(~A)"
    ]

    # print(cnf_form)

    beliefs = []
    beliefs_tmp = []

    stop_counter = 0
    new_statement = ""
    print("Welcome to the belief revision machine, by possibly the most okayest group in intro to AI")
    while new_statement != "exit":
        print("Can only consist of single letters A-Z a-z, '&', '|', '~' and '>>'.")
        new_statement = input("Write a belief: ")
        new_statement = new_statement.upper()
        if check_correct_input(new_statement) and len(new_statement) > 0:
            for expression in expressions:
                cnf_form = parse(expression)
                cnf_form = str(cnf_form)
                print(cnf_form)
                beliefs.append(cnf_form)
                print(beliefs)

                amount = len(re.findall("&", cnf_form)) + 1
                if amount > 1:
                    beliefs.pop()
                    beliefs_tmp = beliefs.copy()
                    newest_beliefs_OG = cnf_form.replace("(", "").replace(")", "")
                    # Text string is 5
                    newest_beliefs = newest_beliefs_OG.split(" & ")
                    for i in range(amount):
                        beliefs_tmp.append(newest_beliefs[i])
                        beliefs_tmp = contraction(beliefs_tmp, 0, {}, sys.maxsize).copy()
                    for i in range(len(beliefs_tmp) - 1, len(beliefs_tmp) - 1 - amount, -1):
                        beliefs_tmp.pop(i)
                    beliefs = beliefs_tmp.copy()
                    beliefs.append(newest_beliefs_OG)
                    print(beliefs)
                else:
                    beliefs = contraction(beliefs, 0, {}, sys.maxsize).copy()
            print(beliefs)

            belief_base = []
            clause = []
            expression = []
