#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>

int key(string key);
int encrypt(string text, string key);

int main(int argc, string argv[])
{
    // Ensure program is used correctly
    if (argc != 2)
    {
        printf("Invalid user input\n");
        return 1;
    }

    // Ensure chiper key is valid
    if (key(argv[1]) == 1)
    {
        printf("Invalid chiper key\n");
        return 1;
    }

    // Promt user for plain text
    string text = get_string("plaintext: ");

    // Encrypt plaintext and print chipertext
    encrypt(text, argv[1]);

    return 0;
}

// Ensure the prompted key is valid
int key(string key)
{
    // Ensure length is exactly 26 letteres
    if (strlen(key) != 26)
    {
        return 1;
    }

    // Ensure its just letters from the english alphabet
    for (int i = 0; i < 26; i++)
    {
        if (isalpha(key[i]) == 0)
        {
            return 1;
        }
    }

    // Ensure key contains only one of all letters
    for (int i = 0; i < 26; i++)
    {
        for (int j = i + 1; j < 26; j++)
        {
            if (key[i] == key[j])
            {
                return 1;
            }
        }
    }

    return 0;
}

// Encrypts given text using promted key
int encrypt(string text, string key)
{
    int chypertext[strlen(text)];
    for (int i = 0; i < strlen(text); i++)
    {
        if (islower(text[i]))
        {
            chypertext[i] = key[text[i] - 97];
            chypertext[i] = tolower(chypertext[i]);
        }
        else if (isupper(text[i]))
        {
            chypertext[i] = key[text[i] - 65];
            chypertext[i] = toupper(chypertext[i]);
        }
        else
        {
            chypertext[i] = text[i];
        }
    }

    // Print the cipher letters to make up the original text
    printf("ciphertext: ");

    for (int i = 0; i < strlen(text); i++)
    {
        printf("%c", chypertext[i]);
    }
    printf("\n");

    return 0;
}