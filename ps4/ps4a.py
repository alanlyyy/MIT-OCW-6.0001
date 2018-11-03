# Problem Set 4A
# Name: Alan Ly
# Collaborators: N/A
# Time Spent: x:xx

#to use random.choice class
import random 
import sys

#increase the recursion limit of the compiler
sys.setrecursionlimit(1000)

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    
    reference:
    https://stackoverflow.com/questions/13109274/python-recursion-permutations
    
    '''
    
    #sequence of permutations
    list_permutations = []
            
    #if all possible sequences have been found return the permutations
    if (len(sequence) == 1):
        
        return [sequence]
       
        
    for char in sequence:
        
        #recursively call the function replace the character in the sequence 
        #with an empty space  
        
        permutations = get_permutations(sequence.replace(char, ""))
        
        #for each item in permutations 
        for permutation in permutations:
            
            #append the current index to the recursive index
            list_permutations.append(char + permutation)
   
    return list_permutations
                
     
        
        
        
    
    
    pass #delete this line and replace with your code here

if __name__ == '__main__':
#    #Test Case #1
    example_input = 'abc'
    print('Input:', example_input)
    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    print('Actual Output:', get_permutations(example_input))
    
    #Test Case #2
    example_input = 'cat'
    print('Input:', example_input)
    print('Expected Output:', ['cat', 'cta', 'act', 'atc', 'tca', 'tac'])
    print('Actual Output:', get_permutations(example_input))
    
    #Test Case #3
    example_input = "Hallu World!"
    print('Input:', example_input)
    print('Expected Output:', ['bae', 'bea', 'abe', 'aeb', 'eba', 'eab'])
    print('Actual Output:', get_permutations(example_input))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)

    pass #delete this line and replace with your code here

