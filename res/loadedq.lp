\Problem name:                                                                  
\FICO Xpress v8.9.2, Community, written 14:20:13, Jun 10, 2020

Minimize
 3 C1 + 4 C2 + 5 C3 + [ 2 C1^2 + 2 C1 * C2 + 2 C1 * C3 + 2 C2^2 + 2 C2 * C3
 + 2 C3^2 ] / 2

Subject To
R1: C1 + C3 >= -2.4 
R2: C1 + C3 >= -3 
R3: C2 + C3 = 4 
R4: C2 + C3 <= 5 

Bounds
-1 <= C1 <= 3 
-1 <= C2 <= 5 
-1 <= C3 <= 8 

End
