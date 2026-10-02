
n = int(input("Enter a number to count up to in reverse"))
i = 0
mylist = []
while i <= n:
    mylist.append(i)
    i = i + 1

mylist.reverse()
print(mylist)