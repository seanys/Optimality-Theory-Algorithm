#!/bin/env python

from __future__ import print_function

import xpress as xp

p = xp.problem()

# 添加多个变量
N = 5
S = range(N)
x = [xp.var(vartype=xp.binary) for i in S] 
p.addVariable(x)

# 添加约束
c0 = xp.Sum(x) <= 10
cc = [x[i]/1.1 <= x[i+1]*2 for i in range(N-1)]
p.addConstraint(c0, cc)

# 设置目标函数
p.setObjective(3 - x[0])

mysol = [0, 0, 1, 1, 1, 1.4]

p.addcols([4], [0, 3], [c0, 4, 2], [-3, 2.4, 1.4], [0], [2], ['YY'], ['B'])
p.write("res/problem1", "lp")

p.solve()



# load a MIP solution
p.loadmipsol([0, 0, 1, 1, 1, 1.4])

p.addqmatrix(1, [x[0], x[3], x[3]], [x[0], x[0], x[3]], [1, -1, 1])

p.addrows(qrtype=['G', 'L'],
          rhs=[4, 4.4],
          mstart=[0, 3, 9],
          mclind=[x[0], x[1], x[2], x[0], x[1], x[2], x[3], x[4], 5],
          dmatval=[1, 2, 3, 4, 5, 6, 7, 8, -3],
          names=['newcon1', 'newcon2'])

p.solve()
p.write("res/amended", "lp")

slacks = []

p.calcslacks(solution=mysol, calculatedslacks=slacks)

print("slacks:", slacks)

p.addcols([4], [0, 3], [c0, 4, 2], [-3, -2, 1], [0], [2], ['p1'], ['I'])
p.addcols([4], [0, 3], [c0, 4, 2], [-3, 2.4, 1.4], [0], [10], ['p2'], ['C'])
p.addcols([4], [0, 3], [c0, 4, 2], [-3, 2, 1], [0], [1], ['p3'], ['S'])
p.addcols([4], [0, 3], [c0, 4, 2], [-3, 2.4, 4], [0], [2], ['p4'], ['P'])
p.addcols([4], [0, 3], [c0, 4, 2], [-3, 2, 1], [0], [2], ['p5'], ['R'])

p.solve()
try:
    print("new solution:", p.getSolution())
except:
    print("could not get solution, perhaps problem is infeasible")