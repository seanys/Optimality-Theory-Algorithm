# example of loadproblem() that adds a quadratic objective
import xpress as xp

p = xp.problem()

# 添加变量和约束
p.loadproblem("",  # probname
              ['G', 'G', 'E', 'L'],  # qrtypes
              [-2.4, -3, 4, 5],  # rhs
              None,  # range
              [3, 4, 5],  # obj
              [0, 2, 4, 8],  # mstart
              None,  # mnel
              [0, 1, 2, 3, 0, 1, 2, 3],  # mrwind
              [1, 1, 1, 1, 1, 1, 1, 1],  # dmatval
              [-1, -1, -1],  # lb
              [3, 5, 8],  # ub
              [0, 0, 0, 1, 1, 2],  # mqobj1
              [0, 1, 2, 1, 2, 2],  # mqobj1
              [2, 1, 1, 2, 1, 2])        # dqe

p.write("res/loadedq", "lp")
p.solve()