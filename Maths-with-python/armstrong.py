def is_armstrong_number(number):
    # Convert the number to a string to get its length
    num_str = str(number)
    num_digits = len(num_str)

    # Initialize sum to store the sum of the powers of digits
    armstrong_sum = 0

    # Calculate the sum of powers of digits
    for digit_char in num_str:
        digit = int(digit_char)
        armstrong_sum += digit ** num_digits

    # Check if the sum equals the original number
    if armstrong_sum == number:
        return True
    else:
        return False

# Example usage:
number = int(input("Enter a number to check if it's an Armstrong number: "))
if is_armstrong_number(number):
    print(number, "is an Armstrong number.")
else:
    print(number, "is not an Armstrong number.")
