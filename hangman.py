import random
import argparse


class Hangman():

    __words = {
        'Animals': ['rabbit', 'horse', 'squirel'],
        'Cars': ['opel', 'tesla', 'lamborghini']
    }

    __debug_words = {
        'Animals': ['hippo'],
        'Cars': ['suzuki'],
    }

    def __init__(self, debug=False):

        self.__debug = debug
        self.__category = self.__get_category()
        self.__word = self.__get_word()
        self.__lives = 6
        self.__letters = []
        self.__guessed_word = ["_"] * len(self.__word)
        self.__finished = False


    def __get_category(self):

        i = 1
        keys = self.__words.keys() if self.__debug else self.__debug_words.keys()
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

        return category


    def __get_word(self):

        if self.__debug:
            words = self.__debug_words[self.__category]
        else:
            words = self.__words[self.__category]
        return random.choice(words)

    def __print(self):
        print("==============")
        print("Category: {}".format(self.__category))
        print("Letters: {}".format(sorted(self.__letters)))
        print("Lives left: {}".format(self.__lives))
        print("Word to guess: {}".format(" ".join(self.__guessed_word)))

    def __get_letter(self):

        self.__letter = None
        while (self.__letter is None):
            letter = raw_input()
            if len(letter) != 1:
                print("Only input of size 1 is acceptable!")
                continue

            if not letter[0].isalpha():
                print("Input is not a letter!")
                continue

            letter = letter.lower()

            if letter in self.__letters:
                print("You've already checked for this letter!")
                continue

            self.__letter = letter

    def __find_occurences(self):
        return [i for i, letter in enumerate(self.__word) if letter == self.__letter]

    def play(self):

        while (not self.__finished):
            self.__print()
            self.__get_letter()

            indexes = self.__find_occurences()

            if len(indexes) != 0:
                for i in indexes:
                    self.__guessed_word[i] = self.__letter
                self.__letters.append(self.__letter)
            else:
                print("You missed!")
                self.__lives -= 1
                self.__letters.append(self.__letter)

            if "".join(self.__guessed_word) == self.__word:
                self.__finished = True
                print("Good job! you won! {} was the word!".format(self.__word))

            if self.__lives == 0:
                self.__finished = True
                print("You lost! Correct answer: {}".format(self.__word))


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-d",
                        help="Turn on debug mode (i.e. 1 word per category)",
                        action='store_true'
                       )
    args = parser.parse_args()

    p = Hangman(args.d)
    p.play()

