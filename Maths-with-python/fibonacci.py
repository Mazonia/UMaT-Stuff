def fibonacci(n):
    fib_series = []
    # First two numbers in the Fibonacci series
    a, b = 0, 1
    # If n is 0, return an empty list
    if n == 0:
        return fib_series
    # If n is 1, return [0]
    elif n == 1:
        return [a]
    else:
        fib_series.append(a)
        fib_series.append(b)
        # Generate Fibonacci series up to n
        while b < n:
            a, b = b, a + b
            if b < n:
                fib_series.append(b)
        return fib_series

# Input from the user
num = int(input("Enter a number to print Fibonacci series up to: "))

# Calculate and print Fibonacci series
fib_series = fibonacci(num)
print("Fibonacci series up to", num, ":", fib_series)
