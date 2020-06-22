\Problem name: noname                                                           
\FICO Xpress v8.9.2, Community, written 17:35:29, Jun 10, 2020

Minimize
 3 - C1 + 4 YY

Subject To
R1: C1 + C2 + C3 + C4 + C5 - 3 YY <= 10 
R2: 0.9090909090909091 C1 - 2 C2 + [ C1^2 - 2 C1 * C4 + C4^2 ] <= 0 
R3: 0.9090909090909091 C2 - 2 C3 + 1.4 YY <= 0 
R4: 0.9090909090909091 C3 - 2 C4 <= 0 
R5: 0.9090909090909091 C4 - 2 C5 + 2.4 YY <= 0 
newcon1: C1 + 2 C2 + 3 C3 >= 4 
newcon2: 4 C1 + 5 C2 + 6 C3 + 7 C4 + 8 C5 - 3 YY <= 4.4 

Bounds

Binaries
C1 C2 C3 C4 C5 YY 

End
