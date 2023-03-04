// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <strings.h>
#include <stdlib.h>
#include <ctype.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 10000;

// Hash table
node *table[N];

// Int for size function
int count = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // Point a cursor to the first node in the correct hash bucket
    node *cursor = malloc(sizeof(node));
    cursor->next = table[hash(word)];

    while (cursor->next != NULL)
    {
        if (strcasecmp(cursor->next->word, word) == 0)
        {
            free(cursor);
            return true;
        }
        else
        {
            cursor->next = cursor->next->next;
        }
    }

    free(cursor);
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // Hash function "djb2" from @SAM4RTH on stackoverflow.com
    unsigned int hash = 5381;
    int c;

    while ((c = *word++))
    {
        if (isupper(c))
        {
            c = c + 32;
        }

        hash = ((hash << 5) + hash) + c; // hash * 33 + c // hash << 5 = hash * 2^5
    }

    return hash % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO

    // Open the dictionary in a file-pointer to read from
    FILE *dnry = fopen(dictionary, "r");

    // Check for a valid file
    if (dnry == NULL)
    {
        return false;
    }

    // Buffer string for reading
    char *buf = malloc(sizeof(char[LENGTH]));

    // Read from the dictionary
    while (fscanf(dnry, "%s", buf) != EOF)
    {
        node *n = malloc(sizeof(node));
        strcpy(n->word, buf);
        n->next = NULL;

        unsigned int hash_n = hash(n->word);

        if (table[hash_n] == NULL)
        {
            table[hash_n] = n;
        }
        else
        {
            n->next = table[hash_n]->next;
            table[hash_n]->next = n;
        }
        count++;
    }

    fclose(dnry);
    free(buf);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < N; i++)
    {
        node *cursor = malloc(sizeof(node));
        node *tmp = malloc(sizeof(node));
        cursor->next = table[i];

        while (cursor->next != NULL)
        {
            tmp->next = cursor->next;
            cursor->next = cursor->next->next;
            free(tmp->next);
        }
        free(tmp);
        free(cursor);
    }

    return true;
}
