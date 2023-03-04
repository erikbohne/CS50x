from cs50 import get_string


def main():
    text = get_string("Text: ")

    # Count characters, words and sentences
    chars = count_chars(text)
    words = count_words(text)
    sentences = count_sentences(text)

    # Calculate the score using the formula
    score = formula(chars, words, sentences)

    # Print the result
    print_result(score)


# Counting the characters of text
def count_chars(text):
    number = 0
    for char in text:
        if char.isalpha():
            number += 1
    return number


# Counting the words of text
def count_words(text):
    number = 1
    for char in text:
        if char == " ":
            number += 1
    return number


# Counting the sentences of text
def count_sentences(text):
    number = 0
    for char in text:
        if char == "." or char == "?" or char == "!":
            number += 1
    return number


# Calculating the formula to find the score
def formula(c, w, s):
    L = c / w * 100
    S = s / w * 100
    score = round((0.0588 * L) - (0.296 * S) - 15.8)
    return score


# Print the correct text based on the score
def print_result(score):
    if score < 1:
        print("Before Grade 1")
    elif score > 16:
        print("Grade 16+")
    else:
        print(f"Grade {score}")


main()    