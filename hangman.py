import random

words = {
    'Animals': ['rabbit', 'horse', 'squirel'],
    'Cars': ['opel', 'tesla', 'lamborghini']
}

def findOccurences(s, ch):
    return [i for i, letter in enumerate(s) if letter == ch]


print("Hello in Hangman! You will have 6 tries to find a\
correct word! Which category you want to try?")

i = 1
keys = words.keys()
for key in keys:
    print("({}) {}".format(i, key))
    i += 1

stop = False
while(not stop):
    try:
        number = input("Type category number:")
    except:
        print("Incorrect input, please try again!")
        continue

    if type(number) != int:
        print("Value must be an Integer!")
        continue

    if number < 1 or number > len(keys):
        print("Value does not match a category!")
        continue

    category = keys[number-1]
    stop = True

size = len(words[category])
print("Alright, you chose {} as a category!".format(category))

stop = False
while(not stop):
    value = raw_input("Choose number between {} ".format(1) + 
                      "and {} or press r for random word:".format(size))
    if value == 'r':
        print("You chose random word, good luck!")
        stop = True
        value = random.randint(1, size)
    else:
        try:
            value = int(value)
        except:
            print("Incorrect input, please try again!")
            continue

        if value < 1 or value > size:
            print("Value out of range, please try again!")
            continue
        else:
            stop = True

word = words[category][value-1]
lives = 6
guessed_word = ["_" for l in word]
finished = False
letters = set()

while (not finished):
    print("==============")
    print("Category: {}".format(category))
    print("Letters: {}".format(sorted(letters)))
    print("Lives left: {}".format(lives))
    print("Word to guess: {}".format(" ".join(guessed_word)))

    letter = raw_input()
    if len(letter) != 1:
        print("Only input of size 1 is acceptable!")
        continue

    if not letter[0].isalpha():
        print("Input is not a letter!")
        continue

    letter = letter.lower()

    if letter in letters:
        print("You've already checked for this letter!")
        continue

    indexes = findOccurences(word, letter)

    if len(indexes) != 0:
        for i in indexes:
            guessed_word[i] = letter
        letters.add(letter)
    else:
        print("You missed!")
        lives = lives - 1
        letters.add(letter)

    if "".join(guessed_word) == word:
        finished = True
        print("Good job! you won! {} was the word!".format(word))

    if lives == 0:
        finished = True
        print("You lost! Correct answer: {}".format(word))
