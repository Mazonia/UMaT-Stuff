# Input from the user
num = int(input("Enter a number: "))

# Initialize sum to 0
sum_of_digits = 0

# Extract digits from the number and add them to the sum
while num > 0:
    # Extract the last digit of the number
    digit = num % 10
    # Add the digit to the sum
    sum_of_digits += digit
    # Remove the last digit from the number
    num //= 10

# Print the sum of digits
print("Sum of digits:", sum_of_digits)


# Input from the user
num = input("Enter a number: ")

# Initialize sum to 0
sum_of_digits = 0

# Iterate through each digit in the number
for digit in num:
    # Convert the digit from string to integer and add it to the sum
    sum_of_digits += int(digit)

# Print the sum of digits
print("Sum of digits:", sum_of_digits)
