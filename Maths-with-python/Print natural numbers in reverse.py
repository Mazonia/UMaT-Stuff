user = input('Enter a number to count down from: ')
n = int(user)
i = n
mylist = []
while i >= 0:
    mylist.append(i)
    i = i - 1

for item in mylist:
    print(item)



