from cs50 import get_int


def main():
    # Promt user for height
    while True:
        height = get_int("Height: ")
        if height > 0 and height < 9:
            break

    # Print blocks
    print_blocks(height)


# Function that prints a pyramid with a given height
def print_blocks(height):
    count = 1
    for i in range(height):
        print(" " * (height - count), end="")
        print("#" * count, end="")
        print(" " * 2, end="")
        print("#" * count)
        count += 1


main()