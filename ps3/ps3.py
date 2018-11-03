# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : <your name>
# Collaborators : <your collaborators>
# Time spent    : <total time>

import math
import random
import string

VOWELS = 'aeiou*'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    #print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    #print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0 #number of letters in the hand
    returns: int >= 0
    """
    
    #converts the word to lowercase
    word = word.lower()
    
    #score of first component
    first_score = 0
    
    #score of second component
    second_score = max([7*len(word) - 3 * (n - len(word)), 1])
    
    #compare each char in the word to the key in the dictionary
    #if char in word matches with key in dictionary grab the score.
    
    for char in word:
        
        if char != '*':
            #for character in SCRABBLE_LETTER_VALUES
            for key in SCRABBLE_LETTER_VALUES:
                #if the character is equal to a key in the dictionary
                if char == key:
                    #add the value to the running score
                    first_score +=  SCRABBLE_LETTER_VALUES[char]
    
    return first_score*second_score
    
    

#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    #hand.keys is a tuple of letters
    for letter in hand.keys(): 
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand={}
    num_vowels = int(math.ceil(n / 3))

    for i in range(num_vowels):
        
        #if there is no asterisk in hand
        if ('*' in hand) == False:
            #append an '*' to the hand dictionary
            hand['*'] = hand.get('*',0) + 1
        else:
            x = random.choice(VOWELS) #vowel = 'aeiou*' in string format
            
            #if x is another asterisk make another choice
            while x == '*':
                x = random.choice(VOWELS)
                
            hand[x] = hand.get(x, 0) + 1

    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS) #consonant is a string
        
        #safe way to access values in dictionary to avoid keyvalue error
        hand[x] = hand.get(x, 0) + 1 
    
    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    #convert word to lower case
    word = word.lower()
    
    #makes a copy of the old hand
    new_hand = dict(hand)
    
    #for character in the word
    for char in word:
        #if key is in the new_hand dictionary
        if char in new_hand:
            
            #if the value of the key is greater than 1
            if new_hand[char] > 1:
                
                #decrement the value
                new_hand[char] -= 1
            else:
                #delete the element from the new_hand dictionary
                del(new_hand[char])
    
    return new_hand

#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    
    #convert word to lowercase
    word = word.lower()
    
    #convert word from string to list
    new_word= []
    for char in word:
        new_word.append(char)
    
    #convert the list form of word to a dictionary
    word_to_dict = get_frequency_dict(new_word)
    
    if word in word_list:
        #for a chracter in the dictionary
        for key in word_to_dict:
            #if the character is not in your hand or the number of characters
            #in your hand is less than the number of characters in the word
            if (key not in hand) or (hand[key] < word_to_dict[key]):
                return False
        return True
    #if the word contains an asterisk
    else:
        #are there matches for the word?
        if are_there_matches(word) == True:
            return True
        else:
            return False
                    
                    
#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
       
    length_of_hand = 0
    
    for num_chars in hand.values():
        length_of_hand += num_chars
        
    return length_of_hand
        

def match_with_asterisks(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
    corresponding letters of other_word, or the letter is the special symbol
    _ , and my_word and other_word are of the same length;
    False otherwise: 
    '''
    #removes white space from the string    
    my_word = my_word.replace(" ","")

    
    if len(my_word) != len(other_word):
        #if my word and other word are not the same length
        return False
    
    else:
        
        for index, my_char in enumerate(my_word,0):
            #if my character is not equal to the other_word character
            if my_char !=  '*':
                
                #if my character is not equal to the other words character or
                #the count of the character in the other character is not the same
                if (my_char != other_word[index] \
                    or my_word.count(my_char) != other_word.count(my_char)):
                   
                    return False
            #the character is an asterisk
            else:
                #is the other_word at that position of the asterisk a vowel?
                if other_word[index] not in VOWELS:
                    return False
        return True
    
def are_there_matches(my_word):
    '''
    my_word: string with * characters, current guess of secret word
    n: integer number of letters left in your hand
    returns: boolean, if word is in wordlist that matches my_word
    Keep in mind that in hangman when a letter is guessed, all the positions
    at which that letter occurs in the secret word are revealed.
    Therefore, the hidden letter(_ ) cannot be one of the letters in the word
    that has already been revealed.
    
    ex of my_word: c*ws, cows, money, m*ney
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
   
    possible_words = []
    same_length_words = []
    
    #find all the other words with the same length as replaced_word (optional)
    for word in load_words():
        if len(word) == len(my_word):
            same_length_words.append(word)
        else:
            continue
    
    #if other_word matches with my_word add to list of possible words 
    for other_word in same_length_words:
        if(match_with_asterisks(my_word, other_word) == True):
            possible_words.append(other_word)
    
    #convert the list of possible words to a string
    possible_words = " ".join(str(x) for x in possible_words)  
    
    if len(possible_words) != 0:
        return True
    else:
        return False
        
def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    
    # BEGIN PSEUDOCODE <-- Remove this comment when you implement this function
    
    # Keep track of the total score
    running_score = 0
    
    handlen = calculate_handlen(hand)
    
    # As long as there are still letters left in the hand:
    while handlen > 0:
    
        # Display the hand
        print("Current hand:")
        display_hand(hand)
        
        # Ask user for input
        user_word = input("Enter word, or '!!' to indicate \
                                                      that you are finished: ")
        # If the input is two exclamation points:
        if user_word == '!!':
            # End the game (break out of the loop)
            break
            
        # Otherwise (the input is not two exclamation points):
        else:
            # If the word is valid:
            if is_valid_word(user_word,hand,word_list):
                # Tell the user how many points the word earned,
                # and the updated total score
                
                running_score += get_word_score(user_word,handlen)
                print("'",user_word,"'", 'earned', \
                                      get_word_score(user_word,handlen), \
                                              'points. Total: ', running_score)
                # Otherwise (the word is not valid):
                # Reject invalid word (print a message)
                
                # update the user's hand by removing the letters of their 
                #inputted word
                hand = update_hand(hand,user_word)
            
            else:
                print("That is not a valid word. Please choose another word.")
            
            

    # Game is over (user entered '!!' or ran out of letters),
    # so tell user the total score
    if calculate_handlen(hand) == 0:
        print("Ran out of letters. Total score: ", running_score," points.")
        print("-------------")
        
    # Return the total score as result of function
    return running_score

#
# Problem #6: Playing a game
# 


#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)2
    """
    
    #make a copy of the old hand
    new_hand = dict(hand)
    
    #number of letters in the hand
    num_letters = 0
    
    #remove the letter from the hand if letter exists in the hand
    if letter in new_hand:
        
        #records number of appearences for the letter
        num_letters += new_hand[letter]
        print(num_letters)
        
        #delete the element from the hand
        del(new_hand[letter])
        
        for index in range(0,num_letters):
            print(index)
            temp_key = random.choice(VOWELS+CONSONANTS)
            
            #while you keep drawing the same letter or selecting a char 
            #already in your hand, make a new choice.
            while (temp_key == letter) or (temp_key in new_hand):    
                temp_key = random.choice(VOWELS+CONSONANTS)
                    
            
            #add the character into the hand and update the value
            new_hand[temp_key] = new_hand.get(temp_key,0) + 1 
    
    return new_hand
  

def replay_score(user_hand, running_score, first_score, replay_flag):
    '''
    The code checks to see if user has selected replay mode. If user selects 
    replay mode, play_hand is ran again. The max value between replay_score and
    first_score will be added to the running score. If replay mode was already
    selected, add the first_score to the running score.
    
    user_hand = dictionary 
    running_score = integer 
    first_score = integer, temporary score
    replay_flag = boolean, checks to see if user selected replay mode 
    
    returns: running_Score and replay_Flag
    '''
    if replay_flag == False:
                    
            user_sel_replay = input("Would you like to replay the hand?")
        
            if user_sel_replay.lower() == "yes":
            
                replay_flag = True
            
                replay_score = play_hand(user_hand,load_words())
            
                if first_score > replay_score:
                    
                    running_score += first_score
            
                else:
                    
                    running_score += replay_score
        
            else:
            
                running_score += first_score
                
    else:
        
            running_score += first_score  
    
    
    return running_score,replay_flag

    
def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    
   #user selects the number of hands play 
    user_select = int(input("Please input the number of hands:"))
    
    #keep a count of the score
    running_score = 0
    
    #make an alias of user_select
    num_hands = user_select
     
    #user subsitution flag
    sub_flag = False 
    
    #user replay selection flag
    replay_flag = False
    
    #while the number of hands is greater than 0
    while num_hands != 0:
        
        #gives user a new hand after every round
        user_hand = deal_hand(HAND_SIZE)
        
        #displays users hand
        display_hand(user_hand)
        
        #if user has not used a subsitution
        if sub_flag == False:
                
            
            option_to_sub = input("Would you like \
                                                  to subsitute a letter? ")
        
            if option_to_sub.lower() == "yes":
            
                sub_flag = True
            
                letter_sub = input("What letter would \
                                           you like to replace?").lower()
            
                #if the letter selected is not in the hand
                while(letter_sub not in user_hand.keys()):
                    
                    print("That is an invalid letter, please try again.")
                    
                    display_hand(user_hand)
                    
                    letter_sub = input("What letter would \
                                           you like to replace?").lower()
                
                
                display_hand(user_hand)
            
                #returns hand with subsituted letter
                user_hand = substitute_hand(user_hand,letter_sub)
                
                running_score += play_hand(user_hand, load_words())

            else:
            
                first_score = play_hand(user_hand,load_words())
                
                #checks to see if a replay has been used
                running_score, replay_flag = replay_score(user_hand, \
                                                         running_score, \
                                                    first_score, replay_flag)                
                num_hands -= 1
      
        else:
            
            if replay_flag == True:
                
                 first_score = play_hand(user_hand,load_words())
                 running_score += first_score
                 num_hands -= 1
            
            else:
                
                first_score = play_hand(user_hand,load_words())
                
                #check to see if user has used replay mode
                running_score, replay_flag = replay_score(user_hand, \
                                                         running_score, \
                                                    first_score, replay_flag)    
                num_hands -= 1
            

    print("Total score over all hands: ", running_score)
                
                
            
            
    


#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
