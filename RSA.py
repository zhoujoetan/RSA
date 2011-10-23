import binascii
import math
import random
   
def euclid(a, b):
    if a < b:
        (a, b) = (b, a) #flip a and b if a is smaller than b
    while 0 != a % b:
        (a, b) = (b, a % b)
    return b

def coprime(L):
    for i in range(len(L)):
        for j in range(i + 1, len(L)):
            if 1 != euclid(L[i], L[j]):
                return False
    return True 

def extendedEuclid(a, b):
    c = []
    isaLarger = True
    if a < b:
        (a, b) = (b, a)
        isaLarger = False
    while 0 != a % b:
        c.insert(0, -(a // b))
        (a, b) = (b, a % b)
    y = 1
    z = c.pop(0)
    for i in range(len(c)):
        (y, z) = (z, c[i] * z + y)
    if isaLarger:
        return (b, y, z)
    else:
        return (b, z, y)

def modInv(a, m):
    if 1 != euclid(a, m):    
        return 0
    else:
        return extendedEuclid(a, m)[1] % m

def crt(L):
    testlist = []
    m = 1
    x = 0
    for i in range(len(L)):
        testlist.append(L[i][1])
        m *= L[i][1]
    if False == coprime(testlist):
        return -1
    else:
        for i in range(len(L)):
            inv_m = m // L[i][1]
            x += L[i][0] * modInv(inv_m, L[i][1]) * inv_m
    return x % m
def euclid(a, b):
    if a < b:
        (a, b) = (b, a) #flip a and b if a is smaller than b
    while 0 != a % b:
        (a, b) = (b, a % b)
    return b

def extractTwos(m):
    '''return (s, d) in which m = 2 ^ s * d'''
    zeros = '0'         #length of zeros in the end 
    binm = bin(m)       #convert m to binary
    while bin(m).endswith(zeros):
        zeros += '0' 
    s = len(zeros) - 1      #s equals to total # of zeros in the end
    d = m // pow(2, s)
    return (s, d)

def int2baseTwo(x):
    '''convert a integer into a binary list in reverse order'''
    binList = []
    while x != 0:
        binList.append(x % 2)
        x = x // 2          #each iteration divided by 2 and keep the remainder
    return binList
       
def modExp(a, d, n):
    '''compute a ^ d mod n'''
    result = 1
    binList = int2baseTwo(d)        #get binary list from d
    for i in binList:
        if i == 1:
            result = (result * a) % n   #calculate the product
        a = a * a % n 
    return result

def millerRabin(n, k):
    '''determine if n is a prime. If True, n is probably a prime,
       if False, n is definitely a composite.'''
    if n > 2 and n % 2 == 0:    #even number which is larger than 2 is composite
        return False
    (s, d) = extractTwos(n - 1)       #extract n - 1 = 2 ^ s * d
    continueFlag = False        #use this flag to break nested loops
    for i in range(k):
        x = random.randint(2, n - 1)   #randomly choose an integer in (2, n - 1)
        while (x % 2 == 0):
            x = random.randint(2, n - 1)   #randomly choose an integer in (2, n - 1)
        x = modExp(x, d, n)      #compute x ^ d mod n
        if x == 1 or x == n - 1:  #1 or n - 1, probably a prime
            continue
        for j in range(1, s):
            x = (x * x) % n       #keep approaching n - 1
            if x == 1:     #n is composite if gets 1 somewhere in the middle
                return False
            elif x == n - 1:   #n is probably a prime if gets n - 1
                continueFlag = True
                break           #break the inner loop
            else:
                pass
        if continueFlag == True:        #break the outer loop
            break
        return False            #cannot get result as n - 1, n is composite
    return True                 #after k loops, consider n to be prime

def primeSieve(k):
    '''return a list of length k + 1 indicating if the index of each position
       is a prime.'''
    primeList = [-1, -1, 1]        #1 and 0 are special, marked as -1
    for i in range(3, k + 1):
        #test if there exists a prime factor in range (2, sqrt(i) + 1)
        for j in range(2, int(math.sqrt(i)) + 2):
            #only test primes
            if primeList[j] == 1 and euclid(i, j) != 1:
                #if there exist a prime factor, mark i as composite
                primeList.append(0)     
                break
        if len(primeList) != i + 1:     #test out all primes, mark i as prime
            primeList.append(1)
    return primeList

def findAPrime(a, b, k):
    '''return a prime integer(trying k times) between a and b'''         
    isPrime = False
    x = random.randint(a, b)    #randomly generate a integer between a and b
    if x % 2 == 0:
        x += 1         #make sure x is odd
    boundry = x + 35 * int(math.log1p(x))   #how far x should look ahead
    #keep trying if x has not crossed the boundry and not a prime
    while not millerRabin(x, k):   
        x += 2
        if x > boundry:     #if x has crossed the boundry(rarely happens!)
            return -1
    return x

def newKey(a, b, k):
    '''generates an RSA encryption/decryption key set.'''
    p = findAPrime(a, b, k)  
    q = findAPrime(a, b, k)     #find two random primes  
    key = p * q
    phi = (p - 1) * (q - 1)
    e = phi
    while (euclid(e, phi) != 1):
        e = random.randint(2, key - 1) #pick a random publick key
    d = modInv(e, phi)    #compute the secret key
    return (key, e, d)

def string2numList(strn):
    '''convert characters to corresponding ascii value'''
    return [num for num in strn.encode()]

def numList2string(L):
    '''convert a list of integer to corresponding string'''
    for i in range(len(L)):
        if L[i] >= 127:
            L[i] =127
    return bytes(L).decode()

def numList2blocks(L, n):
    '''convert a list of integer to base-256 blocks of size n'''
    splitL = [L[i:i+n] for i in range(0, len(L), n)]    #split L into n blocks
    if len(splitL[-1]) < n:
        for i in range(n - len(splitL[-1])):    #padding 0s for the last block
            splitL[-1].append(0)
    #convert each block in splitL to decimal representation of its hex value
    return [int(binascii.hexlify(bytes(blocks)), 16) for blocks in splitL]

def blocks2numList(blocks, n):
    '''convert blocks of size n into a integer list.'''
    numList = []
    for block in blocks:
        hexnum = hex(block)[2:]
        if len(hexnum) % 2 != 0:
            hexnum = '0' + hexnum   #pad 0 to make it a even digit hex number
        #convert the hex value to integer list
        numList += [num for num in bytes.fromhex(hexnum)]
    return numList

def encrypt(message, modN, e, blockSize):
    '''return the ciphertext of a RSA encryption message.'''
    numList = string2numList(message)
    blocks = numList2blocks(numList, blockSize)     #get the message in blocks
    return [modExp(m, e, modN) for m in blocks]

def decrypt(secret, modN, d, blockSize):
    '''return the original message from a given ciphertext.'''
    blocks = [modExp(cipher, d, modN) for cipher in secret]
    numList = blocks2numList(blocks, blockSize)
    return numList2string(numList)
