import sys

from sympy.logic import boolalg

from src.functions.functions import parse, check_correct_input, check_doubles_and_contradictory_statement, contraction
import re

if __name__ == "__main__":

    beliefs = []
    beliefs_tmp = []

    stop_counter = 0
    new_statement = ""
    print("Welcome to the belief revision machine, by possibly the most okayest group in intro to AI")
    while new_statement != "exit":
        print("Can only consist of single letters A-Z a-z(except: e/E, i/I, n/N, o/O, s/S, q/Q, æ/Æ ø/Ø and å/Å),"+ "\n" + "and '&', '|', '~' and '>>'.")
        new_statement = input("Write a belief: ")
        new_statement = new_statement.upper()
        if check_correct_input(new_statement) and len(new_statement) > 0:
            cnf_form = parse(new_statement)
            cnf_form = str(cnf_form)
            print(cnf_form)
            if check_doubles_and_contradictory_statement(cnf_form, beliefs):
                print("Old Belief base:")
                print(beliefs)
                beliefs.append(cnf_form)
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
                else:
                    beliefs = contraction(beliefs, 0, {}, sys.maxsize).copy()
            else:
                print("Contradictory statement or logical equivalent belief already exist in belief base. "
                      "Statement not added to belief base")
            print("New Belief base:")
            print(beliefs)
