import random
random.numbers = []
def add(num1=1, num2=1):
    sum = num1 + num2
    print(sum)

def sub(num1=1, num2=1):
    subt = num1 - num2
    print(subt)
def div(num1=1, num2=1):
    divi =  num1 / num2
    print(divi)
def mult(num1=1, num2=1):
    multi = num1 * num2
    print(multi)
print("Welcome to the SIMPLE CALCULATOR")
print("What would you like to use the calculator for?")
print(" 1. ADD\n", "2. SUBTRACT\n", "3. DIVIDE\n", "4. MULTIPLY\n")
try:
    x = int(input("Enter the number option"))
    number1 = int(input("Enter your first number"))
    number2 = int(input("Enter your second number"))

    if x == "1" or "add" or "ADD":
        add(number1, number2)

    elif x == "2" or "SUBTRACT" or "subtract":
        sub(number1, number2)

    elif x == "3" or "DIVIDE" or "divide":
        div(number1, number2)

    else:
        mult(number1, number2)
except ValueError:
    print("Start over and Enter a number")


