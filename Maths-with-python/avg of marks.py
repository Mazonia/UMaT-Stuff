turns = int(input("How many scores will be input?"))

sum = 0
for i in range(turns):
    x = int(input("Enter your mark"))
    sum += x

print("The sum is ", sum)
average = sum / turns
print("The average is ", average)