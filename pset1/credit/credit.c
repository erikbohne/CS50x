#include <cs50.h>
#include <stdio.h>
#include <math.h>

long card(void);
int valid(long number, int length);
int len(long number);
const char *type(long number, int length);

int main(void)
{
    // Prompt user for a credit card number
    long number = card();

    // Get length of card number
    int length = len(number);

    // Ensure card is valid
    if (valid(number, length) != 1)
    {
        printf("INVALID\n");
        return 0;
    }

    // Print what type of credit card user prompted
    printf("%s\n", type(number, length));

}

// Promt user for a card number
long card(void)
{
    long number;
    do
    {
        // Ask user for a number
        number = get_long("Number: ");
    }
    while (number < 0);

    return number;
}

// Check if the card is valid
int valid(long number, int length)
{
    long curr = 0;
    int sum = 0;
    int product = 0;
    for (int i = 1; i < length + 1; i++)
    {
        curr = number % 10;
        number = number / 10;
        if (i % 2 == 0)
        {
            product = 2 * curr;
            if (product > 9)
            {
                sum = sum + (product % 10) + (product / 10);
            }
            else
            {
                sum = sum + product;
            }
        }
        else
        {
            sum = sum + curr;
        }
    }

    // Check if checksum is valid
    if (sum % 10 == 0)
    {
        return 1;
    }
    else
    {
        return 0;
    }
}

// Calculate length of card number
int len(long number)
{
    int n = 0;
    while (number > 0)
    {
        number = number / 10;
        n++;
    }

    return n;
}

// Identify which type of debit card
const char *type(long number, int length)
{
    int one = number / pow(10, length - 1);
    int two = number / pow(10, length - 2);

    if (one == 4)
    {
        if (length == 13 || length == 16)
        {
            return "VISA";
        }
    }
    else if (two == 34 || two == 37)
    {
        return "AMEX";
    }
    else if (two == 51 || two == 52 || two == 53 || two == 54 || two == 55)
    {
        return "MASTERCARD";
    }

    return "INVALID";
}