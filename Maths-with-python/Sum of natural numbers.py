def sum_of_natural_num():
    n = int(input("Enter a number to get sum up to"))
    i = 0
    sum = 0
    while i < n:
        sum = sum + i
        i = i + 1

    print(i)
    print(sum)
sum_of_natural_num()

def nsum():
    sum1 = 0
    count = 1
    while (count < 10):
        sum1 = sum1 + count
        count = count + 1
    print(count)
    print(sum1)
nsum()