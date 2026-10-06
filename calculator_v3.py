import operator
import math
def main_menu():
    print("Welcome to my calculator!")
    while True:
        #print("Modes available are 'calculator mode' etc.")
        mode = input("What mode would you like to use?")
        if mode.upper().strip() == "CALCULATOR":
            calculator()
        elif mode.upper().strip() == "ADVANCED MATH":
            advanced_math()
        else:
            print("Enter a valid mode")


#Calculator functions
def tokenizer():
    tokens = []
    valid_operations = ("+", "-", "*", "/", "^")
    print("These are the operations that calculator supports: '+', '-', '*', '/', '^'.  For squAre roots, refer to the square root mode.")
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
                    return
            if character in valid_operations or character == "(" or character == ")":
                tokens.append(character)
            else:
                print("Error - Enter valid characters")
                return
    if current_number:
        try:
            tokens.append(float(current_number))
        except ValueError:
            print("Error - Enter valid characters")
            return
    for index, token in enumerate(tokens):
        if token == "-" and index == 0 and index + 1 < len(tokens) and isinstance(tokens[index + 1], float):
            tokens[index + 1] = operator.neg(tokens[index + 1])
            del tokens[index]
        elif token in valid_operations and index == 0:
            if token != "-":
                print('Error - Operations other than "-" at the beginning of the expression is not supported')
                return
            elif token == "-" and index == 0 and index + 1 < len(tokens) and tokens[1] == "(":
                del tokens[0]
                tokens[0:0] = [-1, "*"]
                print(tokens)
        elif token in valid_operations and len(tokens) - 1 == index and index - 1 >= 0 and tokens[index - 1] in valid_operations:
            print("Error - Operations at the end of an expression is not supported")
            return
        elif token == "(" and index + 1 < len(tokens) and tokens[index + 1] == "-" and index + 2 < len(tokens) and isinstance(tokens[index + 2], float):
            tokens[index + 2] = operator.neg(tokens[index + 2])
            del tokens[index + 1]
        elif tokens[index] == "-" and index != 0  and index + 1 < len(tokens) and tokens[index - 1] in valid_operations:
            tokens[index + 1] = operator.neg(tokens[index + 1])
            del tokens[index]
        elif tokens[index] == ")" and index + 1 < len(tokens) and tokens[index + 1] == "(":
            tokens.insert(index + 1, "*")
        elif token in valid_operations and index + 1 < len(tokens) and tokens[index + 1] in valid_operations and tokens[index + 1] != "-":
            print("Error - Multiple Operations in a row are not supported")
            return
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
            return
        elif depth < 0:
            print("Error - Extra closing parenthesis")
            return
        try:    
            for index in range(opening_index + 1, len(tokens)):
                if tokens[index] == ")":
                    closing_index = index
                    break
        except:
            print("Error - Mismatched parentheses")
            return
        for index, token in enumerate(tokens):
            if token == "(" and index + 1 < len(tokens) and tokens[index + 1] == ")":
                print("Error - Empty parenthesis")
                return
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
                try:
                    divisor = expression[operation_position + 1]
                    if divisor == 0:
                        raise ValueError("Division by 0")
                except ValueError as e:
                    print(f"Error - {e}")
                    return
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

def pct():
    while True:    
        print("Would you like to calculate a percentage from a decimal or find a percentage of a number or would you like to return?")
        mode = input("Input 'decimal' or 'number'.")
        if mode.strip().lower() == "decimal":
            try:
                while True:
                    pct_number = input("What number would you like to convert to a percentage?")
                    final_pct = 100 * float(pct_number)
                    print(f"{final_pct}%")
                    break
            except ValueError:
                print("Error - Please enter valid numbers: not expressions")
        elif mode.strip().lower() == "number":
            try:
                while True:
                    base_number = float(input("What is the base number?"))
                    pct = float(input("What percent of that number would you like to calculate?(Input without the % sign)"))
                    final_number = (pct * 0.01) * base_number
                    print(final_number)
                    break
            except ValueError:
                print("Error - Please enter valid numbers: not expressions and dont include the % sign")
        elif mode.strip().lower() == "return":
            return
        else:
            print("Error - Please input 'decimal' or 'number' or 'return'.")
            

def sqrt():
    while True:
        sqrt_number = input("What number would you like to square root?")
        try:
            final_square_root =  math.sqrt(float(sqrt_number))
            print(final_square_root)
        except ValueError:
            print("Error - Please enter valid numbers: not expressions")
        mode = input("Would you like to square root another number? Input 'yes' or 'no'.")
        while True:    
            if mode.strip().lower() == "no":
                return
            elif mode.strip().lower() == "yes":
                continue
            else:
                print("Error - Please input 'yes' or 'no'.")

def abs_value():
    while True:
        abs_value_number = input("What number would you like to get the absolute value of?")
        try:
            abs_value_number =  abs(float(abs_value_number))
            print(abs_value_number)
        except ValueError:
            print("Error - Please enter valid numbers: not expressions")
        while True:
            mode = input("Would you like to get the absolute value of another number? Input 'yes' or 'no'.")
            if mode.strip().lower() == "no":
                return
            elif mode.strip().lower() == "yes":
                break
            else:
                print("Error - Please input 'yes' or 'no'.")

def sci_notation():
    while True:    
        while True:
            sci_notation = input("What number would you like to get the scientific notation of?")
            try:
                sci_notation =  float(sci_notation)
                if sci_notation == 0:
                    print("Error - You cannot get the scientific notation of 0")
                    break
                elif sci_notation >= 10:
                    division_count = 0
                    while sci_notation >= 10:
                        sci_notation = sci_notation/10
                        division_count += 1
                    if division_count == 1:
                        print(f"{sci_notation} × 10¹")
                        break
                    else:
                        unicode_digits = {
                            "0": "\u2070",
                            "1": "\u2071",
                            "2": "\u00b2",
                            "3": "\u00b3",
                            "4": "\u2074",
                            "5": "\u2075",
                            "6": "\u2076",
                            "7": "\u2077",
                            "8": "\u2078",
                            "9": "\u2079"
                            }
                        sci_notation_mult = "".join(unicode_digits[digit] for digit in str(division_count))
                        print(f"{sci_notation} × 10{sci_notation_mult}")
                        break
                elif sci_notation <= -10:
                    mult_count = 0
                    while sci_notation <= -10:
                        sci_notation = sci_notation/10
                        mult_count += 1
                    if mult_count == 1:
                        unicode_digits = {
                            "-": "\u207b",
                            "1": "\u2071",
                            }
                        mult_count = -1
                        sci_notation_mult = "".join(unicode_digits[digit] for digit in str(mult_count))
                        print(f"{sci_notation} × 10{sci_notation_mult}")
                        break
                    else:
                        unicode_digits = {
                            "-": "\u207b",
                            "0": "\u2070",
                            "1": "\u2071",
                            "2": "\u00b2",
                            "3": "\u00b3",
                            "4": "\u2074",
                            "5": "\u2075",
                            "6": "\u2076",
                            "7": "\u2077",
                            "8": "\u2078",
                            "9": "\u2079"
                            }
                        mult_count = mult_count * -1
                        sci_notation_mult = "".join(unicode_digits[digit] for digit in str(mult_count))
                        print(f"{sci_notation} × 10{sci_notation_mult}")
                        break
                else:
                    print(f"{sci_notation} × 10⁰")
            except ValueError:
                print("Error - Please enter valid numbers: not expressions")
        while True:
            mode = input("Would you like to get the scientific notation of another number? Input 'yes' or 'no'.")
            if mode.strip().lower() == "no":
                return
            elif mode.strip().lower() == "yes":
                break
            else:
                print("Error - Please input 'yes' or 'no'.")

def rectangle():
    while True:
        l = input("Please enter the length.")
        w = input("Please enter the width.")
        try:
            l = float(l)
            w = float(w)
            if l <= 0:
                raise ValueError("The length cannot be negative or 0")
            elif w <= 0:
                raise ValueError("The width cannot be negative or 0")
            perimeter = (2 * l) + (2 * w)
            area = l * w
            print(f"The area is, {area}.")
            print(f"The perimeter is, {perimeter}.")
        except ValueError as e:
            print(f"Error - {e}")
        while True:
            mode = input("Would you like to get the area and perimeter of another rectangle? Input 'yes' or 'no'.")
            if mode.strip().lower() == "no":
                return
            elif mode.strip().lower() == "yes":
                break
            else:
                print("Error - Please input 'yes' or 'no'.")

def square():
    while True:
        l = input("Please enter the length.")
        try:
            l = float(l)
            if l <= 0:
                raise ValueError("The length cannot be negative or 0")
            perimeter = 4 * l
            area = l ** 2
            print(f"The area is, {area}.")
            print(f"The perimeter is, {perimeter}.")
        except ValueError as e:
            print(f"Error - {e}")
        while True:
            mode = input("Would you like to get the area and perimeter of another square? Input 'yes' or 'no'.")
            if mode.strip().lower() == "no":
                return
            elif mode.strip().lower() == "yes":
                break
            else:
                print("Error - Please input 'yes' or 'no'.")

def triangle_area():
    while True:    
        b = input("Enter the base length")
        h = input("Enter the height")
        try:
            b = float(b)
            h = float(h)
            if b <= 0:
                raise ValueError("The base cannot be negative or 0")
            elif h <= 0:
                raise ValueError("The height cannot be negative or 0")
            area = 0.5 * b * h
            print(f"The area is, {area}.")
        except ValueError as e:
            print(f"Error - {e}")
        while True:
            mode = input("Would you like to get the area of another triangle? Input 'yes' or 'no'.")
            if mode.strip().lower() == "no":
                return
            elif mode.strip().lower() == "yes":
                break
            else:
                print("Error - Please input 'yes' or 'no'.")

def circle_area():
    while True:    
        r = input("Enter the radius of the circle")
        try:
            r = float(r)
            if r <= 0:
                raise ValueError("The radius cannot be negative or 0")
            area = round(math.pi * r ** 2, 3)
            print(f"The area is, {area}.")
        except ValueError as e:
            print(f"Error - {e}")
        while True:
            mode = input("Would you like to get the area of another circle? Input 'yes' or 'no'.")
            if mode.strip().lower() == "no":
                return
            elif mode.strip().lower() == "yes":
                break
            else:
                print("Error - Please input 'yes' or 'no'.")

def sphere_volume():
    while True:
        r = input("Enter the radius of the sphere")
        try:
            r = float(r)
            if r <= 0:
                raise ValueError("The radius cannot be negative or 0")
            volume = round(4/3 * math.pi* r ** 3, 3)
            print(f"The volume is, {volume}.")
        except ValueError as e:
            print(f"Error - {e}")
        while True:
            mode = input("Would you like to get the volume of another sphere? Input 'yes' or 'no'.")
            if mode.strip().lower() == "no":
                return
            elif mode.strip().lower() == "yes":
                break
            else:
                print("Error - Please input 'yes' or 'no'.")

def cylinder_volume():
    while True:
        r = input("Enter the radius of the cylinder")
        h = input("Enter the height of the cylinder")
        try:
            r = float(r)
            h = float(h)
            if r <= 0:
                raise ValueError("The radius cannot be negative or 0")
            elif h <= 0:
                raise ValueError("The height cannot be negative or 0")
            volume = round(math.pi* r ** 2 * h, 3)
            print(f"The volume is, {volume}.")
        except ValueError as e:
            print(f"Error - {e}")
        while True:
            mode = input("Would you like to get the volume of another cylinder? Input 'yes' or 'no'.")
            if mode.strip().lower() == "no":
                return
            elif mode.strip().lower() == "yes":
                break
            else:
                print("Error - Please input 'yes' or 'no'.")

def cone_volume():
    while True:
        r = input("Enter the radius of the cone")
        h = input("Enter the height of the cone")
        try:
            r = float(r)
            h = float(h)
            if r <= 0:
                raise ValueError("The radius cannot be negative or 0")
            elif h <= 0:
                raise ValueError("The height cannot be negative or 0")
            volume = round(math.pi* r ** 2 * (h/3), 3)
            print(f"The volume is, {volume}.")
        except ValueError as e:
            print(f"Error - {e}")
        while True:
            mode = input("Would you like to get the volume of another cone? Input 'yes' or 'no'.")
            if mode.strip().lower() == "no":
                return
            elif mode.strip().lower() == "yes":
                break
            else:
                print("Error - Please input 'yes' or 'no'.")

def rectangular_prism_volume():
    while True:    
        l = input("Enter the length of the rectangular prism")
        h = input("Enter the height of the rectangular prism")
        w = input("Enter the width of the rectangular prism")
        try:
            l = float(l)
            h = float(h)
            w = float(w)
            if l <= 0:
                raise ValueError("The length cannot be negative or 0")
            elif h <= 0:
                raise ValueError("The height cannot be negative or 0")
            elif w <= 0:
                raise ValueError("The width cannot be negative or 0")
            volume = l * w * h
            surface_area = 2 * ((l * w) + (l * h) + (w * h))
            print(f"The volume is {volume}.")
            print(f"The surface area is {surface_area}.")
        except ValueError as e:
            print(f"Error - {e}")
        while True:
            mode = input("Would you like to get the volume and surface area of another rectangular prism? Input 'yes' or 'no'.")
            if mode.strip().lower() == "no":
                return
            elif mode.strip().lower() == "yes":
                break
            else:
                print("Error - Please input 'yes' or 'no'.")

def triangular_prism_volume():
    while True:    
        b = input("Enter the base of the triangle of the triangular prism")
        h = input("Enter the height of the triangle of the triangular prism")
        l = input("Enter the height of the triangular prism")
        try:
            b = float(b)
            h = float(h)
            l = float(l)
            if b <= 0:
                raise ValueError("The base cannot be negative or 0")
            elif h <= 0:
                raise ValueError("The height cannot be negative or 0")
            elif l <= 0:
                raise ValueError("The length cannot be negative or 0")
            volume = (0.5 * b * h) * l
            print(f"The volume is, {volume}.")
        except ValueError as e:
            print(f"Error - {e}")
        while True:
            mode = input("Would you like to get the volume of another triangular prism? Input 'yes' or 'no'.")
            if mode.strip().lower() == "no":
                return
            elif mode.strip().lower() == "yes":
                break
            else:
                print("Error - Please input 'yes' or 'no'.")

def pythagorean_theorem():
    while True:    
        mode = input("Would you like to solve for the hypotenuse or a leg. Input 'hypotenuse' or 'leg'.")
        if mode.upper().strip() == "LEG":
            a = input("Enter the other leg's length")
            c = input("Enter the hypotenuse length")
            try:
                a = float(a)
                c = float(c)
                if a <= 0 or c <= 0:
                    raise ValueError("No side can be equal to 0")
                elif a >= c:
                    raise ValueError("The leg cannot be greater than or equal to the hypotenuse")
                b_squared = (c ** 2) - (a ** 2)
                b = math.sqrt(b_squared)
                print(f"The legs length is {b}")
            except ValueError as e:
                print(f"Error - {e}")
        elif mode.upper().strip() == "HYPOTENUSE":
            a = input("Enter one leg's length")
            b = input("Enter the other leg's length")
            try:
                a = float(a)
                b = float(b)
                if a <= 0 or b <= 0:
                    raise ValueError("No side can be equal to 0")
                c_squared = (a ** 2) + (b ** 2)
                c = math.sqrt(c_squared)
                print(f"The hypotenuse length is {c}")
            except ValueError as e:
                print(f"Error - {e}")
        else:
            print("Input 'hypotenuse' or 'leg'.")
        while True:
            mode = input("Would you like to solve for another side? Input 'yes' or 'no'.")
            if mode.strip().lower() == "no":
                return
            elif mode.strip().lower() == "yes":
                break
            else:
                print("Error - Please input 'yes' or 'no'.")

def distance():
    while True:    
        x1 = input("Enter x₁")
        y1 = input("Enter y₁")
        x2 = input("Enter x₂")
        y2 = input("Enter y₂")
        try:
            x1 = float(x1)
            y1 = float(y1)
            x2 = float(x2)
            y2 = float(y2)
            d = math.sqrt(((x2 - x1)** 2) + ((y2 - y1) ** 2))
            print(f"The distance between the point ({x1}, {y1}) and the point ({x2}, {y2}) is {d}")
        except ValueError:
            print("Error - Enter valid numbers")
        while True:
            mode = input("Would you like to calculate the distance between another two points? Input 'yes' or 'no'.")
            if mode.strip().lower() == "no":
                return
            elif mode.strip().lower() == "yes":
                break
            else:
                print("Error - Please input 'yes' or 'no'.")

def simple_interest():
    while True:
        try:
            initial_money = float(input("Please enter the initial amount of money"))
            interest_rate = float(input("Please enter the interest rate in decimal form"))
            time = float(input("Enter the time in years that the money will have interest"))
            if initial_money <= 0:
                raise ValueError("The inital amount of money cannot be less than or equal to 0")
            elif interest_rate <= 0:
                raise ValueError("The interest rate cannot be less than or equal to 0")
            elif time <= 0:
                raise ValueError("The number of years cannot be less than or equal to 0")
            interest_money = initial_money * interest_rate * time
            total_money = interest_money + initial_money
            print(f"The amount of money made from interest is {interest_money}")
            print(f"The amount of money overall is {total_money}")
        except ValueError as e:
            print(f"Error - {e}")
        while True:
            mode = input("Would you like to calculate simple interest for another amount of money? Input 'yes' or 'no'.")
            if mode.strip().lower() == "no":
                return
            elif mode.strip().lower() == "yes":
                break
            else:
                print("Error - Please input 'yes' or 'no'.")

def compound_interest():
    while True:    
        try:
            initial_money = float(input("Please enter the initial amount of money"))
            interest_rate = float(input("Please enter the interest rate in decimal form"))
            time = float(input("Enter the time in years that the money will have to compound"))
            if initial_money <= 0:
                raise ValueError("The inital amount of money cannot be less than or equal to 0")
            elif interest_rate <= 0:
                raise ValueError("The interest rate cannot be less than or equal to 0")
            elif time <= 0:
                raise ValueError("The number of years cannot be less than or equal to 0")
            total_money = initial_money * (1 + interest_rate) ** time
            print(f"The amount of money overall is {total_money}")
        except ValueError as e:
            print(f"Error - {e}")
        while True:
            mode = input("Would you like to calculate compound interest for another amount of money? Input 'yes' or 'no'.")
            if mode.strip().lower() == "no":
                return
            elif mode.strip().lower() == "yes":
                break
            else:
                print("Error - Please input 'yes' or 'no'.")

def geometric_formulae():
    while True:
        operation = input("What operation would you like to use?")
        if operation.upper().strip() == "RECTANGLE AREA":
            rectangle()
        elif operation.upper().strip() == "SQUARE AREA":
            square()
        elif operation.upper().strip() == "TRIANGLE AREA":
            triangle_area()
        elif operation.upper().strip() == "CIRCLE AREA":
            circle_area()
        elif operation.upper().strip() == "SPHERE VOLUME":
            sphere_volume()
        elif operation.upper().strip() == "CYLINDER VOLUME":
            cylinder_volume()
        elif operation.upper().strip() == "CONE VOLUME":
            cone_volume()
        elif operation.upper().strip() == "RECTANGULAR PRISM VOLUME":
            rectangular_prism_volume()
        elif operation.upper().strip() == "TRIANGULAR PRISM VOLUME":
            triangular_prism_volume()
        elif operation.upper().strip() == "PYTHAGOREAN THEOREM":
            pythagorean_theorem()
        elif operation.upper().strip() == "RETURN":
            return
        else:
            print("Enter a valid operation or input 'return'.")

def advanced_math():
    while True:
        operation = input("What operation would you like to use?")
        if operation.upper().strip() == "PERCENTAGE":
            pct()
        elif operation.upper().strip() == "SQUARE ROOT":
            sqrt()
        elif operation.upper().strip() == "ABSOLUTE VALUE":
            abs_value()
        elif operation.upper().strip() == "SCIENTIFIC NOTATION":
            sci_notation()
        elif operation.upper().strip() == "GEOMETRIC FORMULAE":
            geometric_formulae()
        elif operation.upper().strip() == "SIMPLE INTEREST":
            simple_interest()
        elif operation.upper().strip() == "COMPOUND INTEREST":
            compound_interest()
        elif operation.upper().strip() == "DISTANCE":
            distance()
        elif operation.upper().strip()== "RETURN":
            return
        else:
            print("Enter a valid operation or input 'return'.")

#Full calculator path returning to main menu
def calculator():
    try:
        tokens = tokenizer()
        tokens = parenthesis(tokens)
        result = calculate_expression(tokens)
        print(float(result[0]))
    except (ValueError, TypeError, IndexError):
        print("Error")
    return

main_menu()