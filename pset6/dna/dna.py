import csv
import sys
import pandas as pd


def main():

    # Ensure correct input
    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py data.csv sequence.txt")

    species = []
    # Read data from database into a list
    with open(sys.argv[1]) as file:
        reader = csv.DictReader(file)
        for word in reader:
            species.append(word)

    # Read the STRs in a list called "strs"
    reader = pd.read_csv(sys.argv[1])
    strs = list(reader.columns)
    # Read the dna to a string
    f = open(sys.argv[2], "r")
    dna = f.read()

    str_dna = {}
    # Get the number of each STR in a dictionary
    for i in range(1, len(species[0]), 1):
        str_dna[strs[i]] = count_strs(dna, strs[i])

    found = False
    for i in range(len(species)):
        if check(strs, str_dna, species[i]):
            print(species[i]["name"])
            found = True
            break
    if not found:
        print("No match")


# Count the max amount of the designated STR in a row
def count_strs(dna, STR):

    # Variables used in the counting
    count = 0
    max_count = 0
    i = 0
    lenght = len(STR)

    # A while True loop that breaks when we have counted all the possible STRs in the DNA
    while True:
        if i >= len(dna) - 1:
            if count > max_count:
                max_count = count
            break

        if dna[i:i + lenght] == STR:
            if count > 0:
                count += 1
                i += lenght
            else:
                count = 1
                i += lenght
        elif count > 0:
            if count > max_count:
                max_count = count
            count = 0
            i += 1
        else:
            i += 1
    return max_count


# Check if the number of each STR is in the database
def check(strs, dna, species):
    count = 0
    for i in range(1, len(strs), 1):
        name = strs[i]
        if int(dna[name]) == int(species[name]):
            count += 1

    if count == len(strs) - 1:
        return True
    else:
        return False


if __name__ == "__main__":
    main()