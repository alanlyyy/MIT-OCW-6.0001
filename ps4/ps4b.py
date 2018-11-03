# Problem Set 4B
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import string

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

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)
        self.copy_valid_words = self.valid_words[:]
        
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
        return self.copy.valid_words

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26
        
        ASCII: A = 65  Z = 90, a = 97 , z = 122

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
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
        
        #builds the alphabetical dictionary before shifting
        for index,char in enumerate(lowercase_letters + uppercase_letters,1):
            alpha_dict[char] =  index
        

        #shift values of dictionary by the value of shift  
        for char in alpha_dict:
            
            #if char is lower case and  index of the char + a 
            #shift >= 26
            if (alpha_dict[char] + shift > 26) and \
                                        (ord(char) > 97 and ord(char) < 123):
                
                #first add the shift to the value of the char
                alpha_dict[char] += shift
                #subtract 26 to circular shift the values
                alpha_dict[char] -= 26
            
            #if char is uppercase and the index + a shift >= 52 
            elif(alpha_dict[char] + shift > 52) and \
                                        (ord(char) > 65 and ord(char) < 91):
                 #first add the shift to the value of the char
                alpha_dict[char] += shift
                #subtract 26 to circular shift the values
                alpha_dict[char] -= 26
            else:
                alpha_dict[char] += shift
                
        return alpha_dict

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        #stores ciphered text message and shift position
        ciphered_shift_position = []
        ciphered_text = [] 
        
        #default dictionary without any shifts used as a reference for 
        #char value positions
        default_dict = self.build_shift_dict(0)
        
        #dictionary with shifted values
        shift_dict = self.build_shift_dict(shift)
        
        #loops through the text message and stores 'values' of 
        #the shift dictionary
        
        for index in range(0,len(self.message_text)):
            
            #if character is in shift_dictionary
            if self.message_text[index] in shift_dict:
                
                #add the value of the shift dictionary of the specified char
                #to a list that stores positions
                ciphered_shift_position.append(shift_dict[self.message_text[index]])

        

        #reverse the default dictionary to flip the values to keys
        reverse_default_dict = dict((v, k) for k, v in default_dict.items()) 
        
        for index in ciphered_shift_position:
            #take the value of the ciphered message dict and find a 
            #'character' which is now a value in reverse dictionary
            # and append that character to the list 'ciphered_text'.
            ciphered_text.append(reverse_default_dict[index])
        
        return ''.join(ciphered_text)
            
        
class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object,    
        This class is used to encode the message. 
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)
            
        '''
        #assign text message as an attribute inside this class
        self.message_text = text
        
        #load valid words into the instance of this class
        self.valid_words = load_words(WORDLIST_FILENAME)
        
        #apply shift attribute to the instance of a class
        self.shift = shift
        
        #builds encryption dictionary from message class
        self.encryption_dict = {k:v for k,v in self.build_shift_dict(self.shift).items()}
        
        #builds encrypted message with the apply_shift function from Message
        #super class.
        self.message_text_encrypted = self.apply_shift(self.shift)

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return self.shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class
        
        Returns: a COPY of self.encryption_dict
        '''
        return self.encryption_dict

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift.        
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift) 
        self.message_text = self.apply_shift(shift)



class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = ""
        self.valid_words = load_words(WORDLIST_FILENAME)
        self.message_list = text.split()
        
        #split the words and append to a list
        #self.valid_words = load_words(get_story_string()).split(' ')

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create 
        the maximum number of valid words, you may choose any of those shifts 
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        max_shift = 26
        shift = 0
        
        decrypt_message_shift =()
        decrypt_words = {}

        #for a word in the story
        for word in self.message_list:
            
            #set the attribute for the instance of the class message_text to word
            self.message_text = word
            
            #loop through each shift value from 1 - 26
            for index in range(1,max_shift):
                
                #if its a valid word add the word to the dictionary
                if is_word(self.valid_words,self.apply_shift(index)):
                    
                    #append an element to the dictionary with a 'text' key
                    #and a 'shift value = index'
                    if len(self.message_list) > 1: 
                        decrypt_words[self.apply_shift(index)] = index
                    else:
                        self.message_text = self.apply_shift(index)
                        shift = index

        
        #get the list of values stored in the decrypt words dictionary
        vals = list(decrypt_words.values())
        print(vals)
        
        
        #loop through dictionary items and append the 'keys' to a tuple.
        if len(list(decrypt_words.keys())) > 1:
            
            #store the max shift value for len(message_text) > 1
            shift = max(vals,key = vals.count)
            
            #if the count of the shift value is greater than one 
            #(found shift value) append the word to the dictionary
            for key,value in decrypt_words.items():
                if (decrypt_words[key] == shift):
                    decrypt_message_shift += (key,)
        else:
            decrypt_message_shift += (self.message_text,)

        return decrypt_message_shift + (shift,)
                

if __name__ == '__main__':

#    #Example test case I (PlaintextMessage)
    plaintext = PlaintextMessage('hello', 2)
    print('Expected Output: jgnnq')
    print('Actual Output:', plaintext.get_message_text_encrypted())
    print("------")
#
#    #Example test case I (CiphertextMessage)
    ciphertext = CiphertextMessage('jgnnq')
    print('Expected Output:', (24, 'hello'))
    print('Actual Output:', ciphertext.decrypt_message())
    print("------")
    
# =============================================================================
# #    #Example test case II (PlaintextMessage)
#     plaintext2 = PlaintextMessage('peanut', 4)
#     print('Expected Output:', plaintext2.apply_shift(4))
#     print('Actual Output:', plaintext2.get_message_text_encrypted())
#     print("------")
# #
# #    #Example test case II (CiphertextMessage)
#     ciphertext2 = CiphertextMessage(plaintext2.get_message_text_encrypted())
#     print('Expected Output:', ciphertext2.decrypt_message())
#     print('Actual Output:', ciphertext2.decrypt_message())
#     print("------")
#     
# #    #Example test case III (PlaintextMessage) Not a word returns nothing
#     plaintext3 = PlaintextMessage('abbc', 4)
#     print('Expected Output:', plaintext3.apply_shift(4))
#     print('Actual Output:', plaintext3.get_message_text_encrypted())
#     print("------")
# #
# #    #Example test case III (CiphertextMessage)
#     ciphertext3 = CiphertextMessage(plaintext3.get_message_text_encrypted())
#     print('Expected Output:', ciphertext3.decrypt_message())
#     print('Actual Output:', ciphertext3.decrypt_message())
#     print("------")
# 
# #    #Example test case IIII (PlaintextMessage) Not a word returns nothing
#     plaintext4 = PlaintextMessage('1234', 4)
#     print('Expected Output:', plaintext4.apply_shift(4))
#     print('Actual Output:', plaintext4.get_message_text_encrypted())
#     print("------")
# #
# #    #Example test case IIII (CiphertextMessage)
#     ciphertext4 = CiphertextMessage(plaintext4.get_message_text_encrypted())
#     print('Expected Output:', ciphertext4.decrypt_message())
#     print('Actual Output:', ciphertext4.decrypt_message())
#     print("------")
# =============================================================================
# =============================================================================
#     #TODO: WRITE YOUR TEST CASES HERE
#     #Test Message class:     
#     print("Test Case 1: (normal)")
#     msg1 = Message('efg')
#     print(msg1.build_shift_dict(22))
#     print(msg1.apply_shift(22))
#     print("---------------")
#     
#     print("Test Case 2:(repeated letters)")
#     msg2 = Message('gghhab')
#     print(msg2.build_shift_dict(2))
#     print(msg2.apply_shift(2))
#     print("---------------")
#     
#     print("Test Case 3:(non alphabetical characters)")
#     msg2 = Message('gg%h%b')
#     print(msg2.build_shift_dict(2))
#     print(msg2.apply_shift(2))
#     print("---------------")
#     #TODO: best shift value and unencrypted story 
#     
# =============================================================================
#   Final Test Case:
    print("Encrypted Output:", get_story_string())    
    print("----------------")
    decrypt_story_text = CiphertextMessage(get_story_string())
    print(decrypt_story_text.decrypt_message())
    print("----------------")

