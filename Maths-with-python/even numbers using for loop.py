evn = int(input("Enter a number to use as a range"))

for i in range(0, evn + 1):
    if i % 2 == 0:
        print(i)
    else:
        print()


def forloop():
    n = int(input("Enter a number to print even numbers in its range"))
    for i in range(0, n, 2):
        print(i)

forloop()