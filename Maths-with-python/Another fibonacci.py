def fibo_numbers():
    length = int(input("Enter the length of number"))
# The first two values
    x = 0
    y = 1
    iteration = 0
# Condition to check if the length has valid input
    if length <= 0:
        print("Please provide a number greater than zero")
    elif length == 1:
        print("This fibonacci sequence has {} element".format(length), ":")
        print(x)
    else:
        print("This fibonacci sequence has {} element".format(length), ":")
    while iteration > length:
        print(x, end=',')
# Modify values
        z = x + y
        x = y = z
        iteration += 1


fibo_numbers()
