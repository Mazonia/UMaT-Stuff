n = int(input("Enter a number to count  sum of even numbers up to"))
i = 0
sum = 0
while i <= n:
    if i % 2 == 0:
        print()
        sum = sum + i
    i = i + 1
print(sum)