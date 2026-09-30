def get_number(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")


def calculator():
    print("Calculator Chatbot")
    print("Enter two numbers and choose an operation:")
    a = get_number("First number: ")
    b = get_number("Second number: ")

    print("Operations: + add, - subtract, * multiply, / divide")
    op = input("Choose operation: ").strip()

    if op == "+":
        result = a + b
    elif op == "-":
        result = a - b
    elif op == "*":
        result = a * b
    elif op == "/":
        if b == 0:
            print("Error: Division by zero is not allowed.")
            return
        result = a / b
    else:
        print("Unknown operation. Please choose +, -, *, or /.")
        return

    print(f"Result: {result}")


if __name__ == "__main__":
    calculator()