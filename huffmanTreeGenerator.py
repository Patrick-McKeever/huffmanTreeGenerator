import numpy as np
import math
from collections import Counter

class node:
    def __init__(self, data, weight, left, right):
        self.data = data
        self.left = left
        self.right = right

        if weight == None:
            self.weight = (self.left.weight) + (self.right.weight)
        else:
            self.weight = weight
    
    #make char -> code mappings as dictionary;
    def encode(self, codePrefix = ''):
        if self.left == None and self.right == None:
            return { self.data : codePrefix }

        return { **self.left.encode(codePrefix + '0'), **self.right.encode(codePrefix + '1') }

#turn dictionary of {char : frequency} pairs into list of nodes;
def nodeFactory(frequencies):
    return [node(char, frequency, None, None) for (char, frequency) in frequencies.items()]

#recursively pretty-print tree;
def printTree(root, space = 0) :
    if (root == None): 
        return
    space += 15
    
    printTree(root.right, space) 
    
    for i in range(15, space): 
        print(end = " ")
        
    string = '%s [%s]' % (root.data, root.weight) if root.data else '%s [%s]---------------' % (root.data, root.weight)
    print(string)
    
    printTree(root.left, space)  

#generate huffman tee of provided string;
def huffmanTreeGenerate(string):
    chars = Counter(string)
            
    charFrequencies = { k:v for (k,v) in sorted(chars.items(), key = lambda x: x[1]) }

    nodes = nodeFactory(charFrequencies)
    
    if len(nodes) == 1:
        return nodes[0]
    
    initialPair = node('', None, nodes[0], nodes[1])
    
    pq = nodes[2:] + [initialPair] #priority queue;
    
    while len(pq) > 1: #until we have a single root note;
        children = []
        for i in range(2):
            indexMin = np.argmin([node.weight for node in pq])
            children.append(pq[indexMin])
            pq.pop(indexMin)
            
        newNode = node('', None, children[0], children[1])
        pq.append(newNode)
        
    return pq[0]

#take string, encode it using pairs provided by huffman tree;
def huffmanEncode(string, mappings):
    returnStr = ''
    for char in string:
        returnStr += mappings[char]
        
    return returnStr

sampleStr = input('Enter phrase:\t')
while sampleStr == '':
    sampleStr = input('Enter a non-empty phrase:\t')
    
huffmanTree = huffmanTreeGenerate(sampleStr)

print('--------------------------HUFFMAN TREE--------------------------')
printTree(huffmanTree)

print('\n\n--------------------------CHARACTER CODES--------------------------')
charMappings = huffmanTree.encode()
print(charMappings)


print('\n\n--------------------------ENCODED STRING--------------------------')
huffmanEncodedStr = huffmanEncode(sampleStr, charMappings)

numberChars = len(set(sampleStr))
fixedWidthCodeLength = math.log(2 ** (numberChars - 1).bit_length(), 2) #take base-2-log of number of unique chars in sampleStr rounded up to nearest power of 2;
fixedWidthStrLength = fixedWidthCodeLength * len(sampleStr)

print('The huffman-encoded version of "%s" is: "%s"' % (sampleStr, huffmanEncodedStr))
print('With %d fixed-width characters each consuming %d bits, representation of this string would have required %d bits. With huffman-encoding, it requires only %d.' 
      % (len(sampleStr), fixedWidthCodeLength, fixedWidthStrLength, len(huffmanEncodedStr))
 )
