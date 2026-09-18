def calculator():
    accepted_operations = ("+", "-", "x", "*", "/")
    expression = []
    #First Number
    while True:
        number = input("Please enter a number.")
        try:
            number = float(number)
            expression.append(number)
            break
        except ValueError:
            print("Please enter a valid number.")
    #First Operation
    while True:
        print("Please enter an operation.")
        operation = input("The options are +, -, x or *, or /.")
        if operation in accepted_operations:
            expression.append(operation)
            break
        else:
            print("Please enter a valid operation.")
    #Second Number
    while True:
        number = input("Please enter a number.")
        if expression[1] == "/" and float(number) == 0:
            print("You cannot divide by zero. Please enter a valid number.")
        else:
            try:
                number = float(number)
                expression.append(number)
                break
            except ValueError:
                print("Please enter a valid number.")
    while True:
        while True:
            print("Please enter an operation or end the expression.")
            operation = input("The options are +, -, x or *, / or end.")
            if operation in accepted_operations:
                expression.append(operation)
                break
            elif operation.upper() == "END":
                #print("Result")
                return expression
            else:
                print("Please enter a valid operation or end the expression.")
        while True:
            number = input("Please enter a number.")
            try: 
                number = float(number)
                if number == 0 and expression[-1] == "/":
                    print("You cannot divide by zero. Please enter a valid number.")
                else:
                    expression.append(number)
                    break
            except ValueError:
                print("Please enter a valid number.")
#Finds places where numbers are meant to be multiplied and multiplies them
def multiplication(expression):
        for value in expression:
            if value == "x":
                operation_position = expression.index("x")
                operation_position = (operation_position)
                factor1 = (expression[operation_position - 1])
                factor2 = (expression[operation_position + 1])
                product = factor1 * factor2
                expression[operation_position - 1 : operation_position + 2] = [product]
            elif value == "*":
                operation_position = expression.index("*")
                operation_position = (operation_position)
                factor1 = (expression[operation_position - 1])
                factor2 = (expression[operation_position + 1])
                product = factor1 * factor2
                expression[operation_position - 1 : operation_position + 2] = [product]
#Finds places where numbers are meant to be divided and divides them
def division(expression):
        for value in expression:
            if value == "/":
                operation_position = expression.index("/")
                operation_position = (operation_position)
                dividend = (expression[operation_position - 1])
                divisor = (expression[operation_position + 1])
                quotient = dividend / divisor
                expression[operation_position - 1 : operation_position + 2] = [quotient]
#Finds places where numbers are meant to be added and adds them
def addition(expression):
        for value in expression:
            if value == "+":
                operation_position = expression.index("+")
                operation_position = (operation_position)
                addend1 = (expression[operation_position - 1])
                addend2 = (expression[operation_position + 1])
                result = addend1 + addend2
                expression[operation_position - 1 : operation_position + 2] = [result]
#Finds places where numbers are meant to be subtracted and subtracts them
def subtraction(expression):
        for value in expression:
            if value == "-":
                operation_position = expression.index("-")
                operation_position = (operation_position)
                minuend = (expression[operation_position - 1])
                subtrahend = (expression[operation_position + 1])
                difference = minuend - subtrahend
                expression[operation_position - 1 : operation_position + 2] = [difference]
#Finds the first operation that needs to be done in PEMDAS order
def find_operations(expression):
    while "x" in expression or "*" in expression or "/" in expression:
        for value in expression:
            if value == "x":
                multiplication(expression)
                break
            elif value == "*":
                multiplication(expression)
                break
            elif value == "/":
                division(expression)
                break
    while "+" in expression or "-" in expression:
        for value in expression:
            if value == "+":
                addition(expression)
                break
            elif value == "-":
                subtraction(expression)
                break

expression = calculator()
find_operations(expression)
print(expression[0])