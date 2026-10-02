accept = int(input("How many numbers do you want to compare?"))
i = 0
num = []
while i < accept:
    number = int(input("Enter a number"))
    num.append(number)
    i += 1

minim = min(num)
print("The minimum number is: ", minim)






