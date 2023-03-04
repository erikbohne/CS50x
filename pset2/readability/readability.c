#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <ctype.h>

int calculate_grade(string text);

int main(void)
{
    // Promt user for text
    string text = get_string("Text: ");

    // Calculate grade of text
    int grade = calculate_grade(text);

    // Print correct grade of text
    if (grade >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", grade);
    }
}

// Calculates the readability of the prompted text
int calculate_grade(string text)
{
    int letters = 0;
    int sentences = 0;
    int words = 1;

    // Count letters, sentences and words
    for (int i = 0; i < strlen(text); i++)
    {
        if (islower(text[i]) || isupper(text[i]))
        {
            letters++;
        }
        else if (text[i] == '!' || text[i] == '.' || text[i] == '?')
        {
            sentences++;
        }
        else if (text[i] == 32)
        {
            words++;
        }
    }

    // Final equation to calculate readability
    float L = letters / (float) words * 100;
    float S = sentences / (float) words * 100;
    float index = 0.0588 * L - 0.296 * S - 15.8;

    return round(index);
}