import re
import random
import sys
import pandas


HW = pandas.read_csv('hangman_words.csv')
lvls = list(HW.columns)
lives = 7


def main():
    lvl = get_lvl()
    wordList = HW[lvl].tolist()
    letterList, displayList = get_word(wordList)

    while True:
        print(" ".join(displayList))
        guess = get_guess()
        check(guess, letterList, displayList, lvl)


def get_lvl():
    global lvls
    while True:
        lvl = input(f"Choose a difficulty level ({lvls[0]}-{lvls[-1]}): ")
        if lvl not in lvls:
            print("Don't be difficult just pick one of the options")
        else:
            return lvl


def get_word(wordList):
    word = random.choice(wordList)
    letterList = list(word)
    displayList = []
    for char in word:
        if char == " ":
            displayList += [" "]
        else:
            displayList += ["_"]
    return letterList, displayList


def get_guess():
    guess = input("Guess a letter: ").strip().upper()
    if guess == "END":
        sys.exit("Ending program...")
    else:
        return guess


def check(guess, letterList, displayList, lvl):
    global lives
    if guess in letterList:
        for letter in letterList:
            if letter == guess:
                indx = letterList.index(letter)
                displayList[indx] = guess
                letterList[indx] = ""
        print("Slayyy")
    elif re.fullmatch(r"[A-Z]", guess):
        lives -= 1
        print("WRONG!")
    else:
        print("Um.. that's not a letter.. ")

    if all((letter == "" or letter == " ") for letter in letterList):
        print(" ".join(displayList))
        win(lvl)
    if lives <= 0:
        sys.exit("You've been hung!")


def win(lvl):
    lvl = int(lvl)
    print("You got it!\n")
    name = input("Enter your name: ")
    pin = input("Enter your PIN: ")
    record = pandas.read_csv("record.csv", dtype={'PIN': str})
    find = record.loc[(record['Name'] == name) & (record['PIN'] == pin), 'Score']

    if find.empty:
        new_row = pandas.DataFrame([{"Name": name, "PIN": pin, "Score": lvl}])
        record = pandas.concat([record, new_row], ignore_index=True)
        print(f"Current Score: {lvl}")
    else:
        row_index = find.index[-1]
        record.loc[row_index, "Score"] += lvl

        cell_value = find.iloc[-1]
        print(f"Current Score: {cell_value + lvl}")
    record.to_csv("record.csv", index=False)
    sys.exit("See you next time!\n")


if __name__ == "__main__":
    main()