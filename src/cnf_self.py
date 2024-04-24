def parse_literal(literal, values_dict):
    """ Parse a literal which might be negated and return its truth value """
    literal = literal.strip()  # Remove any surrounding whitespace
    if literal.startswith('¬'):
        return not values_dict[literal[1:]]
    return values_dict[literal]

def evaluate_clause(clause, values_dict):
    """ Evaluate a disjunctive clause of literals """
    # Remove any surrounding parentheses and split by '∨' (OR operator)
    literals = clause.replace('(', '').replace(')', '').split('∨')
    return any(parse_literal(literal, values_dict) for literal in literals)

def evaluate_cnf(formula, values_dict):
    """ Evaluate the entire CNF formula made up of multiple clauses """
    # Split by '∧' (AND operator) and strip each clause
    clauses = formula.split('∧')
    return all(evaluate_clause(clause.strip(), values_dict) for clause in clauses)

def generate_truth_table(variables, formula):
    """ Generate and print a truth table for the given variables and CNF formula """
    n = len(variables)
    num_combinations = 1 << n  # 2^n combinations

    # Print header
    header = "| " + " | ".join(variables + ['CNF Result']) + " |"
    print(header)
    print("|" + "-" * (len(header) - 2) + "|")

    # Iterate over all combinations of truth values for variables
    for i in range(num_combinations):
        # Generate the current combination of truth values
        values = [(i >> j) & 1 == 1 for j in range(n)]
        values_dict = dict(zip(variables, values))

        # Evaluate the CNF formula with the current combination
        result = evaluate_cnf(formula, values_dict)

        # Print the row of the truth table
        row = "| " + " | ".join(['T' if val else 'F' for val in values] + ['T' if result else 'F']) + " |"
        print(row)

# Example usage
variables = ['p', 'q', 'r']
formula = '(p ∨ ¬q) ∧ (¬p ∨ r)'
generate_truth_table(variables, formula)
