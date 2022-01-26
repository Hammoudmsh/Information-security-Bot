import math
import numpy
import sys
import random


def numrateText(text):
    x = [ord(c) for c in text]
    return x

def enc_cbc(blockSize,Alg):
    pass

def Diff(p, g, open_key_other, my_priv_key):
    B = open_key_other
    a = my_priv_key
    K = BPower(B, a,p)
    return K

from random import randrange, getrandbits

import random
 
def isPrimeMillerRabin(n):
    """
    Miller-Rabin primality test.
 
    A return value of False means n is certainly not prime. A return value of
    True means n is very likely a prime.
    """
    if n!=int(n):
        return False
    n=int(n)
    #Miller-Rabin test for prime
    if n==0 or n==1 or n==4 or n==6 or n==8 or n==9:
        return False
 
    if n==2 or n==3 or n==5 or n==7:
        return True
    s = 0
    d = n-1
    while d%2==0:
        d>>=1
        s+=1
    assert(2**s * d == n-1)
 
    def trial_composite(a):
        if pow(a, d, n) == 1:
            return False
        for i in range(s):
            if pow(a, 2**i * d, n) == n-1:
                return False
        return True  
 
    for i in range(8):#number of trials 
        a = random.randrange(2, n)
        if trial_composite(a):
            return False
 
    return True 

       
def is_prime(n, k=128):
    # Test if n is not even.
    # But care, 2 is prime !
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False
    # find r and s
    s = 0
    r = n - 1
    while r & 1 == 0:
        s += 1
        r //= 2
    # do k tests
    for _ in range(k):
        a = randrange(2, n - 1)
        x = pow(a, r, n)
        if x != 1 and x != n - 1:
            j = 1
            while j < s and x != n - 1:
                x = pow(x, 2, n)
                if x == 1:
                    return False
                j += 1
            if x != n - 1:
                return False
    return True
def generate_prime_candidate(length):
    # generate random bits
    p = getrandbits(length)
    # apply a mask to set MSB and LSB to 1
    p |= (1 << length - 1) | 1
    return p
def generate_prime_number(length = 200):
    p = 4
    while not is_prime(p, 128):
        p = generate_prime_candidate(length)
    return p

def gcd(a, b):     
    if b == 0:
        return a
    else:
        return gcd(b,a % b)
    
def findModInverse(a,m):
    if gcd(a, m) != 1:
        return "Error"
    if a > m:
        x = a
        y = m
    else:
        x = m
        y = a
 
    r = [x, y]
    s = [1, 0]
    t = [0, 1]
    i =1
    rem = 1
    q = [0]
    while rem:
        
        q.append( int(r[i-1]/r[i]) )
        tmp =  r[i-1] % r[i]
        r.append( tmp  )
        s.append( s[i-1]-(q[i]*s[i]))
        t.append( t[i-1]-(q[i]*t[i]))
        rem = tmp
        i = i + 1
    #print('-'*50)
    #print("q  r s  t")
    #for j in range(len(r)-1):
    #    print("{} {} {} {}".format(q[j], r[j], s[j], t[j]))
    
    if a < m :
        z = t[i-1] % m;
    else:
        z = s[i-1] % m; 
    
    w = (a*z) % m
    #print("\n{}*{} mod {} = {} ".format(a,z,m,w))
    #print('-'*50)
    return z
    
def RSA_genrate_keys(length = 200, pqe = ""):
    if pqe == "":
        p = generate_prime_number(length)
        q = generate_prime_number(length)
        n = p*q
        f_n = (p-1)*(q-1)
        while True:
            e = random.randrange(1, f_n)
            if gcd(e, f_n) == 1:
                break
    else:
        (p,q,e) = pqe
        n = p*q
        f_n = (p-1)*(q-1)
    
    d = findModInverse(e, f_n)
    return [(e, n),(d, n)]


def BPower(m,e,n):
    x = 1
    y = m
    while e > 0:
        if e % 2 != 0:
            x = (x * y) % n
        y = (y * y) % n
        e = int(e / 2)
    return x % n

def BPower1(m,e,n):
    
    e1 = bin(e)[2::][::-1]
    
    e = []
    for i in e1:
        e.append(int(i))
    #print(e)
    
    needed = list(numpy.nonzero(e))[0]
    #print(needed)

    indexes =[]
    for i in needed:        
        indexes.append(pow(2,i))
    #print(indexes)
    
    L = len(e)
    values = {}
    for i in range(L):
        if i == 0:
            values[1] =  m % n      
        else:
            values[pow(2,i)] =  pow( values[pow(2,i-1)], 2 ) % n      
    tmp1 = 1
    tmp2 = 1

    indexes1 = indexes[0:-1:1]
    indexes2 = indexes[1:-1:2]
    
    for i in indexes:
        tmp1 = (tmp1 %n) * (values[i]%n) % n
    
    #for i in indexes2:
    #    tmp2 = (tmp2 * values[i]) %  n
    
    tmp = (tmp1* tmp2 )%n
    return tmp

def RSA_enc(m, e, n):
    c = BPower(m, e, n)
    return c  
    
def RSA_dec(c, d, n):
    mr = BPower(c, d, n)
    return mr 

import hashlib
import binascii

length = 20
def gethash(msg, length):
    hash_string = hashlib.sha1(msg.encode('UTF-8')).hexdigest()
    hash_bin = bin(int(hash_string,16))[2::]
    hash_dec = int(hash_bin[0:min(length, len(hash_bin))], 2)
    return hash_dec

def DS_RSA(msg):
    print("\nVerify--------------------------------")
    hash_dec = gethash(msg, length)
    [(e, n), (d, n)] = RSA_genrate_keys(length)
    
    #encrytion
    c = RSA_enc(hash_dec,e, n)
    return (hash_dec, c, (d, n),(e,n))

def DS_RSA_verify(msg, c, priv_key):
    h1 = gethash(msg, length)
    (d, n) = priv_key
    hr = RSA_dec(c, d, n)
    print("\nVerify--------------------------------")
    
    return hr == h1

def AlGamal_Genkeys(pgx = "", length= 5):
    if pgx =="":
        p = generate_prime_number(length)
        g = random.randint(2, p)
        
        x = random.randint(1, p-2)
    else:
        (p, g, x) = pgx
    y = BPower(g, x, p)
    return ((y, g, p),(x, g, p))   #pubpic,private


def AlGamal_Enc(M, Public_key, k = ""): # Public_key = (y, g, p))
    (y, g, p) = Public_key
    if M > p:
        print("error")
        return
    if k == "":
        k = random.randint(1, p-1)
        while( gcd(k, p-1) != 1):
            k = random.randint(2, p-1)
    a = BPower(g, k, p)
    b = ( M * BPower(y, k, p) ) %p
    return (a, b) #(g^k, M*g^ xk )

def AlGamal_Dec(cipher, priv_key):
    (a, b) = cipher
    (x, g, p) = priv_key 
    return (b * findModInverse(BPower(a, x, p), p)) % p


import hashlib
import binascii

length = 20
def DS_Algamal(msg):    
    print("\nSign--------------------------------")
    length = 20
    hash_dec  = gethash(msg, length)
    print("h(m) = ", hash_dec)

    (pub_key, priv_key) = AlGamal_Genkeys(length = length)# ((y, g, p),(x, g, p))   #pubpic,private
        
    #encrytion
    (y, g, p) = pub_key
    (x, g, p) = priv_key
    
    k = random.randint(1, p-1)
    while( gcd(k, p-1) != 1):
        k = random.randint(2, p-1)
    
    a = BPower(g, k, p)
    return ((a, (hash_dec - x*a)*findModInverse(k, p - 1) % (p-1)),pub_key, priv_key)

def DS_Algamal_verify(msg, c, pub_key):
    print("\nVerify--------------------------------")
    a, b = c
    (y, g, p) = pub_key
    hash_dec  = gethash(msg, length)
    print("h(m) = ", hash_dec)
    t1 = ( BPower(y, a, p) * BPower(a, b, p) ) % p
    t2 = BPower(g, hash_dec, p)
    print("\ny^a * a^b = {}^{} * {}^{} mod {}= {}\ng^m = {}^{} = {}".format(y, a, a, b,p, t1, g, m, t2))
    return t1 == t2

def multListByNuM(old_list, NUM):
    new_list = [i * NUM for i in old_list]
    return  new_list

def sumListMod(list1, list2, p):
    zipped_lists = zip(list1, list2)
    sum = [(x + y)% p for (x, y) in zipped_lists]
    return sum

def findItemInList(value, my_list):
    pos = []
    for i,v in enumerate(my_list):
        if v == value:
            pos.append(i)
    return pos

def FindPonts(X, field):
    X = X[::-1]
    z = int((field-1)/2)
    x = list(range(field))
    
    cols = {1:list(range(field))}
    for j in range(2,len(X)):
        tmp = []   
        for i in range(field):
            tmp.append(BPower(i,j,field))
        cols[j] = tmp 
    cols["Y2"] = sumListMod( sumListMod(cols[3], multListByNuM(cols[1],-10), field) ,
                         [-6]*field,
                         field
                        )
    points = []
    for i,v in enumerate(cols["Y2"]):
        list1 = cols[2]
        #list2 = cols[3]
        pos1 = findItemInList(v,list1)
        #pos2 = findItemInList(v, list2)
        """
        if len(pos1) != 0 or len(pos2) != 0:
            print("v",v)
        if len(pos1) != 0:
            print(pos1)
        elif len(pos2) != 0:
            print(pos2)
        """
        for j in pos1:
            points.append((i,j))
    points.append(("inf","inf"))

    return (len(points),points)  


import math
def isgenerator(PointA, X, field):
    GeneratedPoints = []

    tmpPoint = PointA
    GeneratedPoints.append(PointA)
    logger =[]
    i = 2
    while True:
        if i ==2 :
            x, y = PointA
            logger.append("A ({},{})".format(x,y))
            lam = (3*pow(x,2) + X[2]) * findModInverse(2*y, field)
            lam =(lam % field);
            
            x2A = (pow(lam, 2) -(x + x)) % field
            y2A = (-y + lam*(x-x2A)) % field
            logger.append("{}A ({},{}) ({}, {}) {} ({}, {})".format(i, x,y,x,y,lam, x2A, y2A))
            GeneratedPoints.append((x2A,y2A))
        else:
            (x1, y1) = PointA
            (x2, y2) =   GeneratedPoints[-1]
            num = int(y2 - y1) 
            de = int(x2 - x1)
            if de == 0:
                GeneratedPoints.append(("inf","inf"))
                break
                
            elif num % de == 0:
                lam = int(num / de) % field
            else:
                lam = (findModInverse(de, field) * num ) 
                lam = lam %  field 
            xnew = (pow(lam, 2) -(x1 + x2)) % field
            ynew = (-y + lam*(x - xnew))% field
            logger.append("{}A ({}, {}) ({}, {}) {} new ({}, {})".format(i, x1,y1,x2,y2,lam,xnew, ynew))
            GeneratedPoints.append((xnew, ynew))
            
        i = i + 1
    (ll,pp) = FindPonts(X, field)
    return (GeneratedPoints, pp, ll == len(GeneratedPoints),logger )


#-------------------------------------------Monte carlo
