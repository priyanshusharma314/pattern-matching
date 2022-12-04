import random
import math

#To generate random prime less than N
def randPrime(N):
	primes = []
	for q in range(2,N+1):
		if(isPrime(q)):
			primes.append(q)
	return primes[random.randint(0,len(primes)-1)]

# To check if a number is prime
def isPrime(q):
	if(q > 1):
		for i in range(2, int(math.sqrt(q)) + 1):
			if (q % i == 0):
				return False
		return True
	else:
		return False

#pattern matching
def randPatternMatch(eps,p,x):
	N = findN(eps,len(p))
	q = randPrime(N)
	return modPatternMatch(q,p,x)

#pattern matching with wildcard
def randPatternMatchWildcard(eps,p,x):
	N = findN(eps,len(p))
	q = randPrime(N)
	return modPatternMatchWildcard(q,p,x)

# return appropriate N that satisfies the error bounds
def findN(eps,m):
    N=2
    while N>=2:
        if N>(((math.log(N,2))*2*m*(math.log(26,2)))/eps):
            return N
        N=N+1
#out of many values of N satisfying the condition,taking particularly smallest one

      
# Return sorted list of starting indices where p matches x
def modPatternMatch(q,p,x):
    m=len(p)    
    n=len(x)
    f_p=0    #value of f(p)mod q where p is pattern
    for i in range(m):
        f_p=((26*f_p)+(ord(p[i])-65))%q         
    # space complexity:
    # O(log2 q) space will occupied because f(p)mod q can only take values ranging from 0 to q-1
    #time complexity:
    # for loop will run for m times and for every iteration time complexity to calculate f(p) will be O(log2 q)
    # because it's given that arithmetic operations on b bits take Theta(b) time 
    # Thus,time complexity will be O(mlog2 q)    
 
    f_substr=0     #value of f(x[i..(i+m−1)]) where x is text
    result=[]
    #finding value of f(x[i..(i+m−1)]) for first m characters of text-
    i=0
    while i<m and m<=n:
        f_substr=((26*f_substr)+(ord(x[i])-65))%q         
        i=i+1
    if(f_substr==f_p):     #if f(p)=f(x[i..(i+m−1)]),it will be appended to result list
        result.append(0)
    # space complexity:
    # O(log2 q+ log2 m) space will occupied because f(x[i..(i+m−1)])mod q can only take values ranging from 0 to q-1 and i is incremented upto m-1 which requires O(log2 m) space(storing i)
    # time complexity:
    # while loop will run for m times and for every iteration time complexity to calculate f(x[i..(i+m−1)]) will be O(log2 q)
    # Thus,time complexity will be O(mlog2 q)
    
    
    #finding value of f(x[i..(i+m−1)]) for subsequent m characters of text-
    j=1
    while j<n-m+1 and m<=n:
        f_substr=(26*(f_substr-(ord(x[j-1])-65)*(26**(m-1)))+(ord(x[j+m-1])-65))%q       # subtracting the value of f(substr) due to first character of substring and adding value of newly tranversed character
        if(f_substr==f_p):
            result.append(j)      # k is the space for storing output in result list
        j=j+1
    # space complexity:
    # O(log2 q+ log2 (n-m)) space will occupied because f(x[j..(j+m−1)])mod q can only take values ranging from 0 to q-1 and j is incremented upto n-m which requires O(log2 (n-m)) space(storing j)
    # time complexity:
    # This while loop will run for n-m times and for every iteration time complexity to calculate f(x[j..(j+m−1)]) will be O(log2 q)
    # Thus,time complexity will be O((n-m)log2 q)
    
    #THUS,FINAL TIME COMPLEXITY WILL BE O(mlog2 q + m log2 q +(n-m)log2 q) i.e. O((m+n)log2 q)
    #THUS,FINAL SPACE COMPLEXITY WILL BE O(k + log2 q + log2 m + log(n-m)) i.e  O(k+log2 q + log2 n) (taking upper bound of log(n-m))
    return result

# Return sorted list of starting indices where p matches x
def modPatternMatchWildcard(q,p,x):
    n=len(x)
    m=len(p) 
    f_p=0
    wildcard_index=None   
    for i in range(m):
        if p[i]!="?":
            f_p=((26*f_p)+(ord(p[i])-65))%q      #calculating f(p) excluding "?"
        else:
            f_p=(26*f_p)%q
            wildcard_index=i   #stores the index of wildcard in pattern
    # space complexity:
    # O(log2 q+log2 m) space will occupied because f(p)mod q can only take values ranging from 0 to q-1
    #time complexity:
    # for loop will run for m times and for every iteration time complexity to calculate f(p) will be O(log2 q)
    # Thus,time complexity will be O(mlog2 q)

    f_substr=0
    result=[]
    k=0       
    # finding value of f(x[i..(i+m−1)]) for first m characters of text-
    while k<m and m<=n:
        if (k!=wildcard_index):
            f_substr=((26*f_substr)+(ord(x[k])-65))%q
        else:
            f_substr=(f_substr*26)%q
        k=k+1
    if(f_substr==f_p):
        result.append(0)
    j=1
    
    # space complexity:
    # O(log2 q+ log2 m) space will occupied because f(x[k..(k+m−1)])mod q can only take values ranging from 0 to q-1 and k is incremented upto m-1 which requires O(log2 m) space(storing k)
    # time complexity:
    # while loop will run for m times and for every iteration time complexity to calculate f(x[k..(k+m−1)]) will be O(log2 q)
    # Thus,time complexity will be O(mlog2 q) 
    while j<n-m+1 and m<=n:
        if wildcard_index==(m-1):      # when '?' is at last of the pattern
            f_substr=(26*(f_substr-(ord(x[j-1])-65)*(26**(m-1))+ord(x[j+m-2])-65))%q    #treating it as a case of modPatternMatch with pattern length m-1
            #subtracting the value of f(substr) due to first character of substring and adding value of newly tranversed character 
            if(f_substr==f_p):
                result.append(j)     
        else:
            f_substr=(26*(f_substr-(ord(x[wildcard_index+j])-65)*(26**(m-wildcard_index-2))+(ord(x[wildcard_index+j-1])-65)*(26**(m-wildcard_index-1))-(ord(x[j-1])-65)*(26**(m-1)))+(ord(x[j+m-1])-65))%q  
            #subtracting the value of f(substr) due to first character of substring and adding value of newly tranversed character 
            #and subtracting the value of f(substr) due to the character next to wildcard index and adding the value of f(substr) due to character at wildcard index as we move forward in string
            if(f_substr==f_p):
                result.append(j)   
        j=j+1
    # space complexity:
    # O(log2 q+ log2 (n-m)) space will occupied because f(x[j..(j+m−1)])mod q can only take values ranging from 0 to q-1 and j is incremented upto n-m which requires O(log2 (n-m)) space(storing j)
    # time complexity:
    # This while loop will run for n-m times and for every iteration time complexity to calculate f(x[j..(j+m−1)]) will be O(log2 q)
    # Thus,time complexity will be O((n-m)log2 q)
    
    
    #THUS,FINAL TIME COMPLEXITY WILL BE O(mlog2 q + m log2 q +(n-m)log2 q) i.e. O((m+n)log2 q)
    #THUS,FINAL SPACE COMPLEXITY WILL BE O(k + log2 q + log2 m + log(n-m)) i.e  O(k+log2 q + log2 n) (taking upper bound of log(n-m))
    return result