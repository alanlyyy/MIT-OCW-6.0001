# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

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
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    #print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------------------------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
    lowercase letters_guessed: list (of letters), which letters have 
    been guessed so far; assumes that all letters are lowercase returns: 
    boolean, True if all the letters of secret_word are in letters_guessed;
    False otherwise
    '''
    letter_counter = 0
    
    for letter in letters_guessed:
        for secret_letter in secret_word:
            #print(letter, " " , secret_letter)
            if letter == secret_letter:
                letter_counter += 1
    #print(letter_counter)
    
    return letter_counter >= len(secret_word)            
                



def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), 
    and spaces that represents which letters in secret_word have 
    been guessed so far.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    
    secret_list = list(secret_word)
    
    #return list with 'none' data
    guessed_word = ['_']*len(secret_list) 
    
    for letter in letters_guessed:
        for index, secret_letter in enumerate(secret_list,0):
            if letter == secret_letter:
                guessed_word[index] = secret_letter
   
    #returns a string with spaces between char ex) a p p _ _
    return " ".join(str(x) for x in guessed_word)



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which 
    letters have not yet been guessed.
    '''
    #create an alphabet list
    alphabet = []
    for letter in range(97,123): #lowercase a = 97, lowercase z = 123
        alphabet.append(chr(letter))
        
    for letter in letters_guessed:
        for index, character in enumerate(alphabet,0):
            if letter == character:
                alphabet[index] = '_'
                
    #returns alphabet as a string of characters with spaces in between 
    return " ".join(str(x) for x in alphabet)
    
def display_menu(num_guesses, letters_guessed):
    '''
    This function display number of guesses and the letters not chosen yet.
    
    num_guesses: integer
    available_letters: list of letters guessed
    
    '''
    print("You have ",num_guesses," guesses left.")
    print("Available letters:")
    print(get_available_letters(letters_guessed))

def display_wrong_guesses(num_warnings, num_guesses, secret_word, letters_guessed):
    '''
    The function displays messages by measuring the number of warnings and 
    guesses. Decrement either num_guesses or num_warnings depending on scenario.
    
    num_warnings: integer
    num_guesses: integer
    secret_word: string
    letters_guessed: list
    
    '''
    if num_warnings <= 0:
         print("Oops! You've already guessed that letter,", "you have" \
               , num_warnings, "warnings left.")
         print("So you'll lose one guess:" \
                     , get_guessed_word(secret_word,letters_guessed))
         print("------------------------------------------------------")
         
         if num_guesses <= 0:
             return (num_warnings, num_guesses)
         
         else:
             num_guesses -= 1
         
         return (num_warnings, num_guesses)
     
    else:
         num_warnings -= 1
         print("Oops! You've already guessed that letter. You have " \
               , num_warnings," warnings left:")
         print(get_guessed_word(secret_word,letters_guessed))
         print("------------------------------------------------------")
         
         return (num_warnings, num_guesses)

def display_guess_messages(user_guess, num_guesses, secret_word, letters_guessed):
    '''
    Function checks if a character exist in the word, if the character exist 
    display message and return num_guesses. If character does not exist decrement
    the num_guesses
    
    INPUT: 
    user_guess: a single character
    num_guesses: number of guesses user has made
    secret_word: string of characters chosen from word_list
    letters_guessed: running list of character inputs
    
    Output:
    num_guesses a integer

    '''
    if user_guess in list(get_guessed_word(secret_word,letters_guessed)):
        
            print("Good guess: ", \
                         get_guessed_word(secret_word,letters_guessed))
            print("--------------------------------------------------")
            return num_guesses
    else:
            print("Oops! That letter is not in the word", \
                          get_guessed_word(secret_word,letters_guessed))
            print("--------------------------------------------------")
            num_guesses -= 1
            return num_guesses
            
    
    
    
def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
  
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    
    print("Welcome to the game of hangman!")
    print("I am thinking of a word that is",len(secret_word),'letters long.')
    print('------------------------------------------------------------')
    
    guess_counter = 6
    letters_guessed =[] #stores the letters that user has guessed
    warnings = 3
    
    while guess_counter != 0 or \
                        is_word_guessed(secret_word,letters_guessed) == False:
        
        
        #displays menu items 
        display_menu(guess_counter,letters_guessed)
        
        #when number of guesses is 0, user loses.
        if(guess_counter == 0):
            break
        
        #prompts user to make a guess converts to lowercase
        user_guess = input("Please guess a letter:").lower()
        
        #if users guess is already in the list: subtract warnings or guesses
        if user_guess in list(letters_guessed):
            
            
            if warnings <= 0:
                print("Oops! You've already guessed that letter,", "you have" \
                      , warnings, "warnings left.")
                print("So you'll lose one guess:" \
                      , get_guessed_word(secret_word,letters_guessed))
                print("------------------------------------------------------")
                if guess_counter <= 0:
                    break
                else:
                    guess_counter -= 1
            else:
                warnings -= 1
                print("Oops! You've already guessed that letter. You have " \
                                                , warnings," warnings left:")
                print(get_guessed_word(secret_word,letters_guessed))
                print("------------------------------------------------------")
        #if users guess is not in the list of guessed characters
        else:
            #if the users guess is not an 
            #alphabetical character subtract guesses or warnings
            if (ord(user_guess) < 65) or (ord(user_guess) > 122):
                                
                if warnings <= 0:
                     print("Oops! That is not a valid letter,", "you have" \
                                                  , warnings, "warnings left.")
                     print("So you'll lose one guess:", \
                           get_guessed_word(secret_word,letters_guessed))
                     print("-------------------------------------------------")
                     if guess_counter <= 0:
                         break
                     else:
                        guess_counter -= 1
                else:
                     warnings -= 1
                     print("Oops! That is not a valid letter. You have", \
                                                    warnings, "warnings left:")
                     print(get_guessed_word(secret_word,letters_guessed))
                     print("-------------------------------------------------")
                     
            #users guess is an alphabetical character not in the list         
            else:
                
                #add guessed characters into the list of guesses
                letters_guessed.append(user_guess)
                print(letters_guessed)
                
                #compares users guess to secret word
                if user_guess in \
                            list(get_guessed_word(secret_word,letters_guessed)):
                    print("Good guess: ", \
                          get_guessed_word(secret_word,letters_guessed))
                    print("--------------------------------------------------")
                else:
                    print("Oops! That letter is not in the word", \
                          get_guessed_word(secret_word,letters_guessed))
                    print("--------------------------------------------------")
                    guess_counter -= 1
            
                
        if(is_word_guessed(secret_word, letters_guessed) == True):
            break
        
    if(is_word_guessed(secret_word, letters_guessed) == True):
        print("Congratulations, you won!")
    #set - picks out the unique characters and forms a string
    #list - converts the  string to a array
    #len - measure the length of the list to get number of unique characters
        print("Your total score for this game is:", \
                                     guess_counter*len(list(set(secret_word))))
    else:
        print("Sorry, you ran out of guesses. The word was",secret_word,".")
        


# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
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
            if my_char !=  '_':
                
                #if my character is not equal to the other words character or
                #the count of the character in the other character is not the same
                if (my_char != other_word[index] \
                    or my_word.count(my_char) != other_word.count(my_char)):
                   
                    return False
           
        return True


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
    Keep in mind that in hangman when a letter is guessed, all the positions
    at which that letter occurs in the secret word are revealed.
    Therefore, the hidden letter(_ ) cannot be one of the letters in the word
    that has already been revealed.

    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
   
    possible_words = []
    same_length_words = []
    
    #removes white space from the string    
    replaced_word = my_word.replace(" ","")
    

    #find all the other words with the same length as replaced_word (optional)
    for word in load_words():
        if len(word) == len(replaced_word):
            same_length_words.append(word)
        else:
            continue
    
    #if other_word matches with my_word add to list of possible words 
    for other_word in same_length_words:
        if(match_with_gaps(my_word, other_word ) == True):
            possible_words.append(other_word)
    
    #convert the list of possible words to a string
    possible_words = " ".join(str(x) for x in possible_words)  
    
    if len(possible_words) != 0:
        print(possible_words)
    else:
        print("No matches found.")
            




def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. 
        Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    print("Welcome to the game of hangman!")
    print("I am thinking of a word that is",len(secret_word),'letters long.')
    print('------------------------------------------------------------')
    
    guess_counter = 6
    letters_guessed =[] #stores the letters that user has guessed
    warnings = 3
    
    while guess_counter != 0 or \
                        is_word_guessed(secret_word,letters_guessed) == False:
        
        
        #displays menu items 
        display_menu(guess_counter,letters_guessed)
        
        #when number of guesses is 0, user loses.
        if(guess_counter == 0):
            break
        
        #prompts user to make a guess converts to lowercase
        user_guess = input("Please guess a letter:").lower()
        
        #if users guess is already in the list: subtract warnings or guesses
        if user_guess in list(letters_guessed):
            
           warnings, guess_counter = display_wrong_guesses(warnings, \
                                guess_counter, secret_word, letters_guessed)
            
        #if users guess is not in the list of guessed characters
        else:
            
            #if the users guess is not an #alphabetical character 
            #subtract guesses or warnings
            if ((ord(user_guess) < 65) or (ord(user_guess) > 122)) \
                        and ord(user_guess) != 42:
                                
                warnings, guess_counter = display_wrong_guesses(warnings, \
                                guess_counter, secret_word, letters_guessed)
            
            #if asterisk display matching words
            elif(ord(user_guess) == 42):
                show_possible_matches(get_guessed_word(secret_word,letters_guessed))
                print(get_guessed_word(secret_word,letters_guessed))
                print('----------------------------------------')
                     
            #users guess is an alphabetical character not in the list         
            else:
                
                #add guessed characters into the list of guesses
                letters_guessed.append(user_guess)
                print(letters_guessed)
                
                #compares users guess to secret word
                guess_counter = display_guess_messages(user_guess, \
                                            guess_counter, secret_word, \
                                                            letters_guessed)
            
                
        if(is_word_guessed(secret_word, letters_guessed) == True):
            break
        
    if(is_word_guessed(secret_word, letters_guessed) == True):
        print("Congratulations, you won!")
    #set - picks out the unique characters and forms a string
    #list - converts the  string to a array
    #len - measure the length of the list to get number of unique characters
        print("Your total score for this game is:", \
                                     guess_counter*len(list(set(secret_word))))
    else:
        print("Sorry, you ran out of guesses. The word was",secret_word,".")



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    #secret_word = choose_word(wordlist).lower()
    #secret_word = "reject"
    #hangman(secret_word)
    
    #show_possible_matches("pop")
    #print('\n','Test Cases:','\n')
    
    #secret_word = 'apple'
    #letters_guessed = ['e', 'i', 'k', 'p', 'r', 's']
    #print(is_word_guessed(secret_word, letters_guessed) )
    #print(get_guessed_word(secret_word, letters_guessed))
    #print(get_available_letters(letters_guessed))
    #print(get_available_letters([None]*len(secret_word)))
    #print(match_with_gaps('p l a _', 'plan'))
    #show_possible_matches('t _ _ t')
    #show_possible_matches('a _ p l _')
    #show_possible_matches('abbbb_')



    #check if the word is guessed
    #print(is_word_guessed('amazon',['c','e','a','l','p','m'])) #Test case 1
    
    #get guessed word 
    #print(get_guessed_word('amazon',['c','e','a','l','p','m'])) #Test case 2
    
    #available characters
    #print(get_available_letters(['c','e','a','l','p','m'])) #Test case 3

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
