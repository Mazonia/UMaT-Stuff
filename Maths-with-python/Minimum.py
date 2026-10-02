accept = int(input("How many numbers do you want to compare?"))
while i < accept:
    num1 = int(input("Enter a first number"))
    num2 = int(input("Enter a second number"))
    num3 = int(input("Enter a third number"))
    minimum = min(num1, num2, num3)
    print("The smallest number is: ", minimum)
