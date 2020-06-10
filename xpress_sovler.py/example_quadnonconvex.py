#!/bin/env python

# Test problem on a dot product between matrices of scalars and/or of
# variables. Note that the problem cannot be solved by the Optimizer
# as it is nonconvex.

from __future__ import print_function

import xpress as xp
import numpy as np

a = 0.1 + np.arange(21).reshape(3, 7)
y = np.array([xp.var() for i in range(21)]).reshape(3, 7)
x = np.array([xp.var() for i in range(35)]).reshape(7, 5)

p = xp.problem()
p.addVariable(x, y)

p.addConstraint(xp.Dot(y, x) <= 0)
p.addConstraint(xp.Dot(a, x) == 1)

p.setObjective(x[0][0])

p.write("test6-nonconv", "lp")
p.solve()