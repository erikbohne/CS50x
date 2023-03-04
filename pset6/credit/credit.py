from cs50 import get_string
from sys import exit


def main():
    while True:
        number = get_string("Number: ")
        if str.isdecimal(number) and int(number) > 0:
            break

    # Checking lenght of number
    digits = len(number)

    # Creating a checksum variable
    checksum = 0

    # Adding all the odd numbers
    for i in range(digits - 1, -1, -2):
        checksum += int(number[i])

    # Adding all the even numbers after multiplying with 2
    for j in range(digits - 2, -1, -2):
        if (int(number[j]) * 2) < 10:
            checksum += (int(number[j]) * 2)
        else:
            tmp = str(int(number[j]) * 2)
            checksum += int(tmp[0]) + int(tmp[1])

    # Check if it is a valid card based on checksum
    if not valid(checksum):
        exit("INVALID")
    else:
        card = identify_card(number)
        print(card)


# Function that checks if the checksum is valid
def valid(checksum):
    tmp = str(checksum)
    lenght = len(tmp)

    if int(tmp[lenght - 1]) == 0:
        return True
    else:
        return False


# Identify what card it is
def identify_card(number):
    first_two = number[0] + number[1]
    if len(number) == 15 and first_two == "34" or first_two == "37":
        return "AMEX"
    elif len(number) == 16 and int(first_two) > 50 and int(first_two) < 56:
        return "MASTERCARD"
    elif number[0] == "4" and len(number) == 16 or len(number) == 13:
        return "VISA"
    else:
        return "INVALID"


main()    