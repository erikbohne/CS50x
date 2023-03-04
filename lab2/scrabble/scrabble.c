#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Points assigned to each letter of the alphabet
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int compute_score(string word);
int winner(int player1, int player2);

int main(void)
{
    // Get input words from both players
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // Score both words
    int score1 = compute_score(word1);
    printf("%i\n", score1);
    int score2 = compute_score(word2);

    // TODO: Print the winner
    winner(score1, score2);
}

int compute_score(string word)
{
    // TODO: Compute and return score for string
    int sum = 0;
    for (int i = 0; i < strlen(word); i++)
    {
        if (isupper(word[i]))
        {
            sum += POINTS[word[i] - 65];
        }
        else if (islower(word[i]))
        {
            sum += POINTS[word[i] - 97];
        }
    }
    return sum;
}

int winner(int player1, int player2)
{
    if (player1 > player2)
    {
        printf("Player 1 wins!");
        return 1;
    }
    else if (player1 < player2)
    {
        printf("Player 2 wins!");
        return 2;
    }
    else
    {
        printf("Tie!");
        return 0;
    }
}
