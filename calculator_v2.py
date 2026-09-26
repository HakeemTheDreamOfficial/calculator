import operator
import sys
def tokenizer():
    tokens = []
    valid_operations = ("+", "-", "*", "/", "^")
    expression = input("Enter expression:")
    current_number = ""
    for character in expression:
        if character.isspace():
            continue
        elif character.isdigit() or character == ".":
            current_number += character
        else:
            if current_number:
                try:
                    tokens.append(float(current_number))
                    current_number = ""
                except ValueError:
                    print("Error - Enter valid characters")
                    sys.exit(0)
            if character in valid_operations or character == "(" or character == ")":
                tokens.append(character)
            else:
                print("Error - Enter valid characters")
                sys.exit(0)
    if current_number:
        try:
            tokens.append(float(current_number))
        except ValueError:
            print("Error - Enter valid characters")
            sys.exit(0)
    for index, token in enumerate(tokens):
        if token in valid_operations and index == 0:
            if token != "-":
                print('Error - Operations other than "-" at the beginning of the expression is not supported')
                sys.exit(0)
        elif token in valid_operations and len(tokens) - 1 == index:
            print("Error - Operations at the end of an expression is not supported")
            sys.exit(0)
        elif token in valid_operations and tokens[index + 1] in valid_operations:
            if tokens[index + 1] != "-":
                print("Error - Multiple Operations in a row are not supported")
                sys.exit(0)
            else:
                pass
    for index, token in enumerate(tokens):
        if token == "-" and index == 0:
            tokens[1] = operator.neg(tokens[1])
            del tokens[0]
        elif token == "(" and tokens[index + 1] == "-":
            tokens[index + 2] = operator.neg(tokens[index + 2])
            del tokens[index + 1]
        elif tokens[index] == "-" and index != 0 and tokens[index - 1] in valid_operations:
            tokens[index + 1] = operator.neg(tokens[index + 1])
            del tokens[index]
    return tokens

def parenthesis(tokens):
    while "(" in tokens or ")" in tokens:
        depth = 0
        deepest_depth = 0
        #Represents the index of the deepest open parenthesis
        opening_index = None
        # Represents the index of the closing parenthesis matching the deepest opening parenthesis
        closing_index = None
        for index, token in enumerate(tokens):
            if token == "(":
                depth += 1
                if depth > deepest_depth:
                    deepest_depth = depth
                    opening_index = index
            elif token == ")":
                depth -= 1
        if depth > 0:
            print("Error - Extra opening parenthesis")
            sys.exit(0)
        elif depth < 0:
            print("Error - Extra closing parenthesis")
            sys.exit(0)
        for index in range(opening_index + 1, len(tokens)):
            if tokens[index] == ")":
                closing_index = index
                break
        parenthesis_slice = tokens[opening_index + 1:closing_index]
        result = calculate_expression(parenthesis_slice)
        tokens[opening_index:closing_index + 1] = result
    return tokens

def calculate_expression(expression):
    while "^" in expression:
        operation_position = expression.index("^")
        base = expression[operation_position - 1]
        exponent = expression[operation_position + 1]
        result = base ** exponent
        expression[operation_position - 1:operation_position + 2] = [result]
    while "*" in expression or "/" in expression:
        for value in expression:
            if value == "*":
                operation_position = expression.index("*")
                factor1 = expression[operation_position - 1]
                factor2 = expression[operation_position + 1]
                product = factor1 * factor2
                expression[operation_position - 1:operation_position + 2] = [product]
                break
            elif value == "/":
                operation_position = expression.index("/")
                dividend = expression[operation_position - 1]
                divisor = expression[operation_position + 1]
                if divisor == 0:
                    result = "Error - Division by 0"
                    return result
                quotient = dividend / divisor
                expression[operation_position - 1:operation_position + 2] = [quotient]
                break
    while "+" in expression or "-" in expression:
        for value in expression:
            if value == "+":
                operation_position = expression.index("+")
                number1 = expression[operation_position - 1]
                number2 = expression[operation_position + 1]
                result = number1 + number2
                expression[operation_position - 1:operation_position + 2] = [result]
                break
            elif value == "-":
                operation_position = expression.index("-")
                number1 = expression[operation_position - 1]
                number2 = expression[operation_position + 1]
                result = number1 - number2
                expression[operation_position - 1:operation_position + 2] = [result]
                break
    return expression
tokens = tokenizer()
tokens = parenthesis(tokens)
result = calculate_expression(tokens)
print(float(result[0]))