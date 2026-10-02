accept = int(input("How many numbers do you want to compare?"))
i = 0
num = []
while i < accept:
    number = int(input("Enter a number"))
    num.append(number)
    i += 1

maxum = max(num)
print("The maximum number is: ", maxum)






