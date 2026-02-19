
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        print("Error: Cannot divide by zero!")
        return None  # Return None or raise an exception to prevent division
    return a / b
history = []

def calculate(num1, num2, operation):
    result = None
    if operation == 'add':
        result = add(num1, num2)
    elif operation == 'subtract':
        result = subtract(num1, num2)
    elif operation == 'multiply':
        result = multiply(num1, num2)
    elif operation == 'divide':
        result = divide(num1, num2)
    else:
        print(f"Error: Invalid operation '{operation}'")
        return None

    if result is not None:
        history_entry = f"{num1} {get_operator_symbol(operation)} {num2} = {result}"
        history.append(history_entry)
    return result

def get_operator_symbol(operation):
    if operation == 'add':
        return '+'
    elif operation == 'subtract':
        return '-'
    elif operation == 'multiply':
        return '*'
    elif operation == 'divide':
        return '/'
    return ''

print(f"Calculation: 10 + 5 = {calculate(10, 5, 'add')}")
print(f"Calculation: 20 - 7 = {calculate(20, 7, 'subtract')}")
print(f"Calculation: 4 * 6 = {calculate(4, 6, 'multiply')}")
print(f"Calculation: 100 / 4 = {calculate(100, 4, 'divide')}")
print(f"Calculation: 10 / 0 = {calculate(10, 0, 'divide')}")

print("\n--- Calculation History ---")
for entry in history:
    print(entry)

def show_history():
    print("\n--- Calculation History ---")
    if not history:
        print("History is empty.")
        return
    for entry in history:
        print(entry)

def clear_history():
    global history
    history = []
    print("History cleared.")

# Clear history to start fresh for this sequence
clear_history()

print(f"Calculation 1: 15 + 7 = {calculate(15, 7, 'add')}")
print(f"Calculation 2: 30 - 12 = {calculate(30, 12, 'subtract')}")
print(f"Calculation 3: 5 * 9 = {calculate(5, 9, 'multiply')}")
show_history()

print(f"Calculation 4: 50 / 5 = {calculate(50, 5, 'divide')}")
print(f"Calculation 5: 100 + 25 = {calculate(100, 25, 'add')}")
print(f"Calculation 6: 75 - 10 = {calculate(75, 10, 'subtract')}")
show_history()

print(f"Calculation 7: 12 * 3 = {calculate(12, 3, 'multiply')}")
print(f"Calculation 8: 20 / 0 = {calculate(20, 0, 'divide')}") # Division by zero
print(f"Calculation 9: 60 / 10 = {calculate(60, 10, 'divide')}")
show_history()

print(f"Calculation 10: 8 + 4 = {calculate(8, 4, 'add')}")
show_history()