import unittest
from math_suite import (
    is_armstrong, fibonacci_sequence, factorial, is_prime,
    sum_of_digits, count_even_odd, calculate_discount, average_marks,
    simple_calculator, print_multiplication_table
)

class MathSuiteTests(unittest.TestCase):
    def test_armstrong(self):
        self.assertTrue(is_armstrong(153))
        self.assertTrue(is_armstrong(371))
        self.assertFalse(is_armstrong(123))

    def test_fibonacci(self):
        self.assertEqual(fibonacci_sequence(5), [0, 1, 1, 2, 3])
        self.assertEqual(fibonacci_sequence(1), [0])
        self.assertEqual(fibonacci_sequence(0), [])

    def test_factorial(self):
        self.assertEqual(factorial(5), 120)
        self.assertEqual(factorial(0), 1)
        with self.assertRaises(ValueError):
            factorial(-1)

    def test_is_prime(self):
        self.assertTrue(is_prime(2))
        self.assertTrue(is_prime(17))
        self.assertFalse(is_prime(4))
        self.assertFalse(is_prime(1))

    def test_sum_of_digits(self):
        self.assertEqual(sum_of_digits(1234), 10)
        self.assertEqual(sum_of_digits(0), 0)

    def test_count_even_odd(self):
        res = count_even_odd([1, 2, 3, 4, 5, 6])
        self.assertEqual(res['even'], 3)
        self.assertEqual(res['odd'], 3)

    def test_calculator(self):
        self.assertEqual(simple_calculator(10, 5, '+'), 15)
        self.assertEqual(simple_calculator(10, 5, '/'), 2)
        with self.assertRaises(ZeroDivisionError):
            simple_calculator(10, 0, '/')

    def test_discount(self):
        res = calculate_discount(100, 20)
        self.assertEqual(res['final_price'], 80)

if __name__ == '__main__':
    unittest.main()
