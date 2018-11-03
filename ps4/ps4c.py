# Problem Set 4C
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import string
from ps4a import get_permutations

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    
    #print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    #print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

# you may find these constants helpful
VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'

class SubMessage(object):
    def __init__(self, text):
        '''
        Initializes a SubMessage object
                
        text (string): the message's text

        A SubMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)
    
    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        return self.valid_words[:]
                
    def build_transpose_dict(self, vowels_permutation):
        '''
        vowels_permutation (string): a string containing a permutation of vowels (a, e, i, o, u)
        
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to an
        uppercase and lowercase letter, respectively. Vowels are shuffled 
        according to vowels_permutation. The first letter in vowels_permutation 
        corresponds to a, the second to e, and so on in the order a, e, i, o, u.
        The consonants remain the same. The dictionary should have 52 
        keys of all the uppercase letters and all the lowercase letters.

        Example: When input "eaiuo":
        Mapping is a->e, e->a, i->i, o->u, u->o
        and "Hello World!" maps to "Hallu Wurld!"

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
#==============================================================================        
        alpha_dict = {}
        lowercase_letters = []
        uppercase_letters = []
        
        #append lowercase characters
        for value in range(97,123):
            lowercase_letters.append(chr(value))
        #print(lowercase_letters)
        
        #append UPPERcase characters
        for value in range(65,91):
            uppercase_letters.append(chr(value))
        #print(uppercase_letters)
        
        #builds the alphabetical dictionary before encrypting
        for index,char in enumerate(lowercase_letters + uppercase_letters,1):
            alpha_dict[char] =  char
        
        #maps the vowels of the permutation to the reference string of vowels
        #ex) eaiuo -> aeiou
        for index,vowel in enumerate(vowels_permutation,0):
            alpha_dict[vowel.lower()] = VOWELS_LOWER[index]
            alpha_dict[vowel.upper()] = VOWELS_UPPER[index]
            
        
        return alpha_dict

            
    def apply_transpose(self, transpose_dict):
        '''
        transpose_dict (dict): a transpose dictionary
        
        Returns: an encrypted version of the message text, based 
        on the dictionary
        '''
        
        list_message_text = list(self.message_text)
        
        for index,char in enumerate(list_message_text,0):
            
            #if char is a vowel
            if (char in VOWELS_LOWER) or (char in VOWELS_UPPER):
                
                #replace the char with a mapped value of the char found
                #in transpose dictionary
                list_message_text[index] = transpose_dict[char]
                
        return ''.join(list_message_text)
        
class EncryptedSubMessage(SubMessage):
    def __init__(self, text):
        '''
        Initializes an EncryptedSubMessage object

        text (string): the encrypted message text

        An EncryptedSubMessage object inherits from SubMessage and has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words =load_words(WORDLIST_FILENAME)
        self.message_list = []
        
    def decrypt_message(self):
        '''
        Attempt to decrypt the encrypted message 
        
        Idea is to go through each permutation of the vowels and test it
        on the encrypted message. For each permutation, check how many
        words in the decrypted text are valid English words, and return
        the decrypted message with the most English words.
        
        If no good permutations are found (i.e. no permutations result in 
        at least 1 valid word), return the original string. If there are
        multiple permutations that yield the maximum number of words, return any
        one of them.

        Returns: the best decrypted message    
        
        Hint: use your function from Part 4A
        '''
        #stores the decrypted message
        decrypt_words = []
        
        #get all the permutation sets for lower case vowels
        permutation_list = get_permutations(VOWELS_LOWER)


        for permutation in permutation_list:
            
            #get the encrypted string
            self.message_text = self.apply_transpose(self.build_transpose_dict(permutation))
            
            #split the string by spaces and append to a list
            self.message_list = self.message_text.split()
            
            #loop through the list of words in the list
            for word in self.message_list:
                
               #add the word to decrypt words if the word is valid
               if is_word(load_words(WORDLIST_FILENAME),word):
                   decrypt_words.append(word)
            
            #if the length of decrypt words is not equal to the splitted string
            #clear the list after the iteration
            if len(decrypt_words) != len(self.message_list):
                decrypt_words = []
            
            else:
            #word is found break out of the loop and return the string
                break
        
        #if decrypt words is empty, the message is non-decryptable
        if len(decrypt_words) < 1: 
            return self.message_text
        
        else:
            #return the decrypted message
            return ' '.join(decrypt_words)
    

if __name__ == '__main__':
#==============================================================================    
    #Test Case Change SubMessage
    # Example test case
    message = SubMessage("Hello World!")
    permutation = "eaiuo"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "I em")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())
    
    # Example test case 2
    message = SubMessage("Yes Please!")
    permutation = "eaiuo"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Yas Plaesa")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())
    
    # Example test case 3
    message = SubMessage("Dragon Slayer!")
    permutation = "eaiuo"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Dregun Sleyar!")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())
 #=============================================================================    
    #Test Case change permutation
    message = SubMessage("Hello World!")
    permutation = "ouiao"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "I em")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())

    
    # Example test case 2
    message = SubMessage("Yes Please!")
    permutation = "ouiao"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Yus Pluosu")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())
    
    
    # Example test case 3
    message = SubMessage("Dragon Slayer!")
    permutation = "ouiao"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Drogan Sloyur!")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())

    