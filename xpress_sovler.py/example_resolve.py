#
# test-resolve.py
#
# Reads a problem solves it, then adds a constraint and re-solves it
#

from __future__ import print_function

import xpress

p = xpress.problem()

p.read("example.lp")
p.solve()
print("solution of the original problem: ", p.getVariable(), "-->",
      p.getSolution())

x = p.getVariable()
p.addConstraint(xpress.Sum(x) <= 1.1)
p.solve()
print("New solution: ", p.getSolution())