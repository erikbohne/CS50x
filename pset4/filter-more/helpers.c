#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    float avrg;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Calculating the average Red, Green and Blue value and setting alle values to the newly found average
            avrg = (float)(image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3;
            image[i][j].rgbtBlue = round(avrg);
            image[i][j].rgbtGreen = round(avrg);
            image[i][j].rgbtRed = round(avrg);
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // Create a temp for the sorting
    RGBTRIPLE temp;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            // Sort the first pixel in the row with the last one, the second pixel with the second last etc...
            temp = image[i][width - (j + 1)];
            image[i][width - (j + 1)] = image[i][j];
            image[i][j] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Copy all values for colors in image to use in calculating average
    RGBTRIPLE temp_i[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            temp_i[i][j].rgbtBlue = image[i][j].rgbtBlue;
            temp_i[i][j].rgbtGreen = image[i][j].rgbtGreen;
            temp_i[i][j].rgbtRed = image[i][j].rgbtRed;
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Create variables to store sum of RGB values.
            float sumB = 0;
            float sumG = 0;
            float sumR = 0;
            float pixels = 0;
            for (int n = -1; n < 2; n++)
            {
                // Check that the row is actually in the picture and not outside the edges
                if (i + n >= 0 && i + n < height)
                {
                    // Check that the coulmn is in the picture on left side
                    if (j - 1 >= 0)
                    {
                        sumB += temp_i[i + n][j - 1].rgbtBlue;
                        sumG += temp_i[i + n][j - 1].rgbtGreen;
                        sumR += temp_i[i + n][j - 1].rgbtRed;
                        pixels ++;
                    }
                    sumB += temp_i[i + n][j].rgbtBlue;
                    sumG += temp_i[i + n][j].rgbtGreen;
                    sumR += temp_i[i + n][j].rgbtRed;
                    pixels ++;

                    // Check that the coulmn is in the picture on right side
                    if (j + 1 < width)
                    {
                        sumB += temp_i[i + n][j + 1].rgbtBlue;
                        sumG += temp_i[i + n][j + 1].rgbtGreen;
                        sumR += temp_i[i + n][j + 1].rgbtRed;
                        pixels ++;
                    }
                }
            }
            // Give the picture it's new color values after finding average.
            image[i][j].rgbtBlue = (int) round(sumB / pixels);
            image[i][j].rgbtGreen = (int) round(sumG / pixels);
            image[i][j].rgbtRed = (int) round(sumR / pixels);
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    // Copy all values for colors in image to use in calculating average
    RGBTRIPLE temp_i[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            temp_i[i][j].rgbtBlue = image[i][j].rgbtBlue;
            temp_i[i][j].rgbtGreen = image[i][j].rgbtGreen;
            temp_i[i][j].rgbtRed = image[i][j].rgbtRed;
        }
    }
    // Create a factor to be used in the calculation depending on which pixel we are on in the 3x3 grid
    int factor;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Calculate the Gx
            float sumBx = 0;
            float sumGx = 0;
            float sumRx = 0;
            for (int n = -1; n < 2; n++)
            {
                // If the we are on the first row (n == -1) or on the last row (n == 1) the factor is 1, and if not it is 2
                if (n == -1 || n == 1)
                {
                    factor = 1;
                }
                else
                {
                    factor = 2;
                }
                // If the pixels are in the 3x3 grid they are multiplied by the factor and then added to the total sum of the color channel
                if (i + n >= 0 && i + n < height)
                {
                    if (j - 1 >= 0)
                    {
                        sumBx += -1 * factor * temp_i[i + n][j - 1].rgbtBlue;
                        sumGx += -1 * factor * temp_i[i + n][j - 1].rgbtGreen;
                        sumRx += -1 * factor * temp_i[i + n][j - 1].rgbtRed;
                    }
                    if (j + 1 < width)
                    {
                        sumBx += factor * temp_i[i + n][j + 1].rgbtBlue;
                        sumGx += factor * temp_i[i + n][j + 1].rgbtGreen;
                        sumRx += factor * temp_i[i + n][j + 1].rgbtRed;
                    }
                }
            }
            // Calculate Gy
            float sumBy = 0;
            float sumGy = 0;
            float sumRy = 0;
            for (int n = -1; n < 2; n++)
            {
                // If the we are on the first column (n == -1) or on the last column (n == 1) the factor is 1, and if not it is 2
                if (n == -1 || n == 1)
                {
                    factor = 1;
                }
                else
                {
                    factor = 2;
                }
                // If the pixels are in the 3x3 grid they are multiplied by the factor and then added to the total sum of the color channel
                if (j + n >= 0 && j + n < width)
                {
                    if (i - 1 >= 0)
                    {
                        sumBy += -1 * factor * temp_i[i - 1][j + n].rgbtBlue;
                        sumGy += -1 * factor * temp_i[i - 1][j + n].rgbtGreen;
                        sumRy += -1 * factor * temp_i[i - 1][j + n].rgbtRed;
                    }
                    if (i + 1 < height)
                    {
                        sumBy += factor * temp_i[i + 1][j + n].rgbtBlue;
                        sumGy += factor * temp_i[i + 1][j + n].rgbtGreen;
                        sumRy += factor * temp_i[i + 1][j + n].rgbtRed;
                    }
                }
            }
            // Check to see if the value is above our max Blue value, and if so set it to max (255)
            if (round(sqrt(sumBx * sumBx + sumBy * sumBy)) > 255)
            {
                image[i][j].rgbtBlue = 255;
            }
            else
            {
                image[i][j].rgbtBlue = round(sqrt(sumBx * sumBx + sumBy * sumBy));
            }
            // Check to see if the value is above our max Green value, and if so set it to max (255)
            if (round(sqrt(sumGx * sumGx + sumGy * sumGy)) > 255)
            {
                image[i][j].rgbtGreen = 255;
            }
            else
            {
                image[i][j].rgbtGreen = round(sqrt(sumGx * sumGx + sumGy * sumGy));
            }
            // Check to see if the value is above our max Red value, and if so set it to max (255)
            if (round(sqrt(sumRx * sumRx + sumRy * sumRy)) > 255)
            {
                image[i][j].rgbtRed = 255;
            }
            else
            {
                image[i][j].rgbtRed = round(sqrt(sumRx * sumRx + sumRy * sumRy));
            }
        }
    }
    return;
}
