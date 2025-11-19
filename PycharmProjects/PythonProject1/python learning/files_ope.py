
l1 = [2,4,3]
l2 = [5,6,4]
reverse_number1 = l1[::-1]
reverse_number2 = l2[::-1]
print(reverse_number1)
print(reverse_number2)
first_number = int(''.join(map(str, reverse_number1)))
second_number = int(''.join(map(str,reverse_number2)))
final_number = first_number + second_number

reversed_digits = [int(digit) for digit in str(final_number)[::-1]]
print(reversed_digits)





