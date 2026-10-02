
num = int(input("Enter a number: "))
is_prime = True
divisor = 2

while divisor <= num // 2:
    if num % divisor == 0:
        is_prime = False
        break
    divisor += 1

if is_prime:
    print(num, "is a prime number.")
else:
    print(num, "is not a prime number.")