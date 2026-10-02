def factorial(n):
    # Base case: If the number is 0 or 1, factorial is 1
    if n == 0 or n == 1:
        return 1

    # Initialize the factorial value to 1
    fact = 1

    # Multiply all numbers from 1 to n
    for i in range(2, n + 1):
        fact *= i

    return fact


# Input from the user
num = int(input("Enter a number to find its factorial: "))

# Calculate factorial and print the result
result = factorial(num)
print("Factorial of", num, "is", result)
