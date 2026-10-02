# Input from the user
num = int(input("Enter a number: "))

# Print the multiplication table
print("Multiplication Table for", num)
for i in range(1, 11):
    print(num, "x", i, "=", num * i)
