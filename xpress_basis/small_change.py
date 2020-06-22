# 修改参数系数的案例

import xpress as xp

x = xp.var()
y = xp.var()

cons1 = x + y >= 2
upperlim = 2*x + y <= 3

p = xp.problem()

p.addVariable(x, y)
p.setObjective((x-4)**2 + (y-1)**2)
p.addConstraint(cons1, upperlim)

p.write('res/original', 'lp')

p.chgcoef(cons1, x, 3)  # 修改x在cons1的系数为3
p.chgcoef(1, 0, 4)      # 修改第1个约束upperlim中y的系数为4

p.write('res/changed', 'lp')