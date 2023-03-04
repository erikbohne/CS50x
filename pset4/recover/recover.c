#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdint.h>

#define BLOCK 512

typedef uint8_t BYTE;

bool jpeg(int a, int b, int c, int d);

int main(int argc, char *argv[])
{
    // Check if command line argument is used correctly
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    // Rembember filename
    char *infile = argv[1];

    // Open file and check if it is valid
    FILE *input = fopen(infile, "r");
    if (input == NULL)
    {
        printf("Could not open %s.\n", infile);
        return 1;
    }

    // Variable to keep count of jpeg number
    int j_num = 0;
    char *filename = malloc(sizeof(BYTE));

    // Read infile's JPEGHEADER
    BYTE buffer[BLOCK];
    while (fread(buffer, sizeof(BYTE), BLOCK, input) == BLOCK)
    {
        // Check for start of new JPEG
        if (jpeg(buffer[0], buffer[1], buffer[2], buffer[3]))
        {
            // Create a new jpeg file
            sprintf(filename, "%03i.jpg", j_num);
            FILE *img = fopen(filename, "w");
            fwrite(buffer, sizeof(BYTE), BLOCK, img);
            fclose(img);
            j_num ++;
        }
        // Check for ongoing JPEG
        else if (j_num > 0)
        {
            FILE *img = fopen(filename, "a");
            fwrite(buffer, sizeof(BYTE), BLOCK, img);
            fclose(img);
        }
    }
    free(filename);
    return 0;
}

// Function to check if the block of bytes is the start of a new jpeg file
bool jpeg(int a, int b, int c, int d)
{
    if (a == 0xff && b == 0xd8 && c == 0xff && (d & 0xf0) == 0xe0)
    {
        return true;
    }
    return false;
}