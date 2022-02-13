import numpy as np
import pandas as pd
import random

class WordInfo:
    def __init__(self, letters, letterPts, possWords, bestWords, maxPoints):
        self.letters = letters
        self.letterPts = letterPts
        self.possWords = possWords
        self.bestWords = bestWords
        self.maxPoints = maxPoints

def create_word_info():
    
    dictionary = pd.read_csv("https://raw.githubusercontent.com/zeisler/scrabble/master/db/dictionary.csv", header = None)
    dictionary.columns = ["Alpha. Order"]
    dictionary = dictionary[dictionary["Alpha. Order"].isna() == False]   
    
    # Orders words and creates column of ordered words in dictionary
    ordered_words = []
    ordered_words = sorted(dictionary["Alpha. Order"].values, key = len)
    dictionary["Length Order"] = ordered_words
    
    letter_bank = {"a": 1, "b": 3, "c": 3, "d": 2, "e": 1, "f": 4, "g": 2, "h": 4, "i": 1, "j": 8, "k": 5, "l": 1, "m": 3, "n": 1, "o": 1, "p": 3, "q": 10, "r": 1, "s": 1, "t": 1, "u": 1, "v": 4, "w": 4, "x": 8, "y": 4, "z": 10}
    picked_letters = random.sample(list(letter_bank), 10)
    
    # Ensures that there are vowels in the picked letters. If not, replaces random letter(s) with a vowel, calculates letter points
    vowels = ["a", "e", "i", "o", "u"]
    
    num_vowels = 0
    
    for vowel in vowels:
        if vowel in picked_letters:
            num_vowels += 1
        if num_vowels == 2:
            break
    
    if (num_vowels < 2):
        
        if (num_vowels == 0):
            
            to_be_replaced = random.sample(range(len(picked_letters)), 2)
            to_replace = random.sample(vowels, 2)
                                           
            for i in range(2):
                picked_letters[to_be_replaced[i]] = to_replace[i]
        
        else:
            curr_vowel = ""
            
            for i in range(len(picked_letters)):
                if picked_letters[i] in vowels:
                    curr_vowel = picked_letters.pop(i)
                    break
            
            other_vowels = [v for v in vowels if v != curr_vowel]
            
            picked_letters[random.choice(range(len(picked_letters)))] = random.choice(other_vowels)
            
            picked_letters.insert(random.choice(range(len(picked_letters))), curr_vowel)
    
    letter_pts = [letter_bank[letter] for letter in picked_letters]
    
    # Method that returns all the words of the inputted length 
    def words_of_length(desired_length):
        return [word for word in dictionary["Length Order"].values if len(word) == desired_length]
    
    # List of words of inputted length
    all_words = words_of_length(3) + words_of_length(4) + words_of_length(5)
    
    # Returns all words that are possible with given letters
    
    final_words = all_words.copy()

    for word in all_words:

        for char in word:
            if char not in picked_letters:
                final_words.remove(word)
                break
    
    if (len(final_words) == 0):
        create_word_info(picked_length)
    else:
    
        # Calculates point tally of a word

        def point_tally(word):
            tally = 0

            for char in word: 
                tally += letter_bank[char]

            return tally

        # Returns best possible words and associated point tally

        def word_tallies(word_list):

            words = {}

            for word in word_list:
                words[word] = point_tally(word)
                        
            return dict(sorted(words.items(), key=lambda word: word[1], reverse = True))

        poss_words = word_tallies(final_words)

        if len(poss_words) >= 5:
            best_words = list(poss_words.items())[:5]
        else:
            best_words = list(poss_words.items())
            
        max_points = 0
        
        for pair in best_words:
            max_points += pair[1]
        
        newGame = WordInfo(picked_letters, letter_pts, poss_words, best_words, max_points)
        return newGame

def score_gauge(pts, top):
        
    response = ""
        
    score_pos = round((63*pts/top),2)

    if (pts >= 0.8*top):
        response = "You're a master!"
    elif (pts >= 0.6*top):
        response = "Genius!"
    elif (pts >= 0.4*top):
        response = "Wow!"
    elif (pts >= 0.2*top):
        response = "Great!"
    elif (pts > 0):
        response = "Nice!" 
            
    return response, score_pos
