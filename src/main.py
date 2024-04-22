from sympy.logic import boolalg




"""
(A | B ->  C)
 = not(A | B) | C
 = not(A) & not(B) | C 
 
 

A ^ B -> not(C)
 = not(A ^ B) | not(C)
 = not(A) | not(B) | not(C)
 
 K1
 
 K2
 
 
 
 1. req = (not(A) | not(C)) & not(B)
 2. req = A & B
 
 
 (b | ~a) & (~a | ~c)
 (not(A) | not(C)) & (not(B) | C ) -> not(A) 
 
 k1:
 a = 0 => c = 1|0
 a = 1 => c = 0
 
 k2:
 b = 0 => c = 0|1
 b = 1 => c = 1
 
 k1 & k2:
  a = 0 => c = 1|0 && b = 0 => c = 0|1
  a = 0 => c = 1|0 && b = 1 => c = 1
  a = 1 => c = 0 && b = 0 => c = 0|1
  a = 1 => c = 0 && b = 1 => c = 1
  
req 2: 
  a = 0 => b = 1|0 && c = 1|0
  a = 1 => b = 0 => c = 1|0
  b = 0 => c = 1|0 && c = 1|0
  
 
 if 
 2. req = A cannot do
 or 
 2. req = (A & B & C) no can do!
 
 A = 0
 B = 1 or 0
 C = not(b) if b != 1

Prio:
1. Do nothing
2. Contraction
3. Revision

points (?):


 Generally: 
 (K1 & K2 & ...  & KN
 
 
 
 left from req 1 = 
 
 
"""

"""
 1. BELIEFSET{{a},{b}, {AND(a,b) => c},  NOT(c)}
 if we now gat the new belief of NOT(c) then we can revise the set 
 of belief in the following of two ways: 
 
    - we remove the a will result in {AND(a,b) => NOT(c)} and NOT(c) being true
    - same if we remove b
    - if we remove the entire implecation {AND(a,b) => NOT(c)}
 
"""