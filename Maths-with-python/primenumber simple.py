number = int(input("Enter a number"))

def primenumber(number):
    isPrime = True
    if number <= 1:
        isPrime = False
    for i in range(2,number):
        if number % i == 0:
            isPrime = False
    if isPrime:
        print("It is a prime number")
    else:
        print("it is not a prime number")

primenumber(number)