#include <cs50.h>
#include <stdio.h>

// Defining functions before main
int space(int n);
int hash(int n);

int main(void)
{
    // Promt user for height
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);

    // Print hashes with promted height
    for (int i = 1; i < height + 1; i++)
    {
        space(height - i);
        hash(i + 1);
        space(2);
        hash(i + 1);
        printf("\n");
    }
}

// Function that prints n spaces
int space(n)
{
    for (int i = 1; i < n + 1; i++)
    {
        printf(" ");
    }
    return 1;
}

// Function that prints n hashes
int hash(n)
{
    for (int i = 1; i < n; i++)
    {
        printf("#");
    }
    return 1;
}