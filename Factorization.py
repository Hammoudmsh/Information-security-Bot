import sys
import locale
import random


def isqrt(n):
    x=n
    y=(x+n//x)//2
    while(y<x):
        x=y
        y=(x+n//x)//2
    return x
def factorFermat(n):
    t0=isqrt(n)+1
    counter=0
    t=t0+counter
    temp=isqrt((t*t)-n)
    while((temp*temp)!=((t*t)-n)):
        counter+=1
        t=t0+counter
        temp=isqrt((t*t)-n)
    s=temp
    p=t+s
    q=t-s
    return p,q
#----------------------------------------------------------------------------------

# Python code for Pollard p-1 
# factorization Method
   
# importing "math" for 
# calculating GCD
import math
   
# importing "sympy" for 
# checking prime
import sympy
# function to generate 
# prime factors
def pollardOne(n,r0):
   
    # defining base
    a = r0
    # defining exponent
    i = 2
    # iterate till a prime factor is obtained
    while(True):
        # recomputing a as required
        a = (a**i) % n
        # finding gcd of a-1 and n
        # using math function
        d = math.gcd((a-1), n)
        # check if factor obtained
        if (d > 1):
            #return the factor
            return d
            break
        # else increase exponent by one 
        # for next round
        i += 1
def factoPollard(n,r0):
    # temporarily storing n
    num = n       
    # list for storing prime factors
    ans = []
    # iterated till all prime factors
    # are obtained
    while(True):
        # function call
        d = pollardOne(num,r0)
        # add obtained factor to list
        ans.append(d)
        # reduce n
        r = int(num/d)
        # check for prime using sympy
        if(sympy.isprime(r)):
            # both prime factors obtained
            ans.append(r)
            break
        # reduced n is not prime, so repeat
        else:
            num = r
    return ans



class FactorError(Exception):
    def __init__(self, value):
        self.value = value 
    def __str__(self):
        return repr(self.value)
"""
def miller_rabin_pass(a, n):
    d = n - 1
    s = 0
    while d % 2 == 0:
        d >>= 1
        s += 1

    a_to_power = pow(a, d, n)
    if a_to_power == 1:
        return True
    for i in xrange(s-1):
        if a_to_power == n - 1:
            return True
        a_to_power = (a_to_power * a_to_power) % n
    return a_to_power == n - 1

def isprime(n):
    for repeat in xrange(20):
        a = 0
        while a == 0:
            a = random.randrange(n)
        if not miller_rabin_pass(a, n):
            return False
    return True
"""


def gcd(a, b):
    while b != 0:
        a, b = b, a%b
    return a 

def findfactor(n):
    for c in range(1, 50):
        x = y = random.randint(1, n-1)
        x = (x * x + c) % n
        y = (y * y + c) % n
        y = (y * y + c) % n
    while True:
        t = gcd(n, abs(x-y))
        if t == 1:
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
        elif t == n:
            break
        else:
            return t
    raise FactorError("couldn't find a factor.")
    
def factor(n):
    r = []
    while True:
        if isprime(n):
            r.append(n)
            break
        try:
            f = findfactor(n)
            r.append(f)
            n = n / f
        except FactorError:
            r.append(n)
            break
    r.sort()
    return r 

locale.setlocale(locale.LC_ALL, "")

def doit(n):
    flist = factor(n)
    #print locale.format("%d", n, True), "="
    for f in flist:
        #print "\t%s" % locale.format("%d", f, True)
        print(f)
    return "dd"
