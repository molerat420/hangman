import csv
import re
import random
import sys
import pandas

WL = []
DL = []
lives = 6


def main():
    get_lvl()
    game_loop()


def get_lvl():
    global WL
    global DL
    lvl = str(input("Choose a difficulty level (1|2|3): "))
    if lvl != "1" and lvl != "2" and lvl != "3":
        print("Don't be difficult just pick one of the numbers")
        main()
    else:
        wordList = []
        with open('hangman_words.csv') as hCSV:
            reader = csv.DictReader(hCSV)
            for row in reader:
                wordTemp = row[lvl]
                wordList += [wordTemp]
        
        word = random.choice(wordList)
        for char in word:
            WL += [char]
            if char == " ":
                DL += [" "]
            else:
                DL += ["_"]
        

def game_loop():
    global DL
    print(" ".join(DL))
    guess = get_guess()
    check(guess)


def get_guess():
    guess = input("Guess a letter: ").strip().upper()
    if guess == "END":
        sys.exit()
    else:
        return guess


def check(guess):
    global WL
    global DL
    global lives
    if guess in WL:
        for l in WL:
            if l == guess:
                num = WL.index(l)
                DL[num] = guess
                WL[num] = ""
        print("Slayyy")
    elif re.fullmatch(r"[A-Z]", guess):
        lives -= 1
        print("WRONG!")
    else:
        print("Um.. that's not a letter.. ")

    if all(item == "" for item in WL):
        print(" ".join(DL))
        print("You did it!")
        win()
    if lives <= 0:
        print("You've been hung!")
        sys.exit()

    game_loop()


def win():
    name = input("Enter your name: ")
    df = pandas.read_csv("record.csv")
    row = df[df["Name"] == name]

    if not (row.index.to_list()):
        PIN = input("Create a PIN: ")
        new_user(name, PIN)
    else:
        PIN = str(input("Enter your PIN: "))
        row2 = df[df["PIN"] == PIN]
        if not (row2.index.to_list()):
            new_user(name, PIN)

    sys.exit()

def new_user(name, PIN):
    print(f"{name}: 1")
    sys.exit()


    


if __name__ == "__main__":
    main()
