#### Solves the problem:
#### min c1*x + c2*y
#### st  A1*x + A2*y <=b (m constraints)
#### x binary n1-dimensional vector
#### y >=0 continuous n2-dimensional vector

import xpress as xp
import sys

# 初始化问题参数
c1 = [1,6,5,7]                    # n1 x 1
c2 = [9,3,0,2,3]                  # n2 x 1
b  = [-3,-4,1,4,5]                   # m  x 1
A1 = [[0, -2, 3, 2],
      [-5, 0, -3, 1],
      [1, 0, 4, -2],
      [0, -3, 4, -1],
      [-5, -4, 3, 0]]
A2 = [[3, 4, 2, 0, -5],
      [0, 2, 3, -2, 1],
      [2, 0, 1, -3, -5],
      [-5, 3, -2, -3, 0],
      [-2, 3, -1, 2, -4]]
m  = len(b)
n1 = len(c1)
n2 = len(c2)

# 绝对精准度
ObjAbsAccuracy=0.00001

# 定义问题
p = xp.problem()

# 定义全部变量
x = [xp.var(vartype=xp.binary) for i in range(n1)]
y = [xp.var() for i in range(n2)] #positive real variable
p.addVariable(x,y)

# 定义约束
constr = [xp.Sum(A1[ii][jj]*x[jj] for jj in range(n1)) +                       \
          xp.Sum(A2[ii][jj]*y[jj] for jj in range(n2))                         \
                        <=b[ii] for ii in range(m)]
p.addConstraint(constr)

# 定义目标函数
p.setObjective(xp.Sum(c1[jj]*x[jj] for jj in range(n1)) +                      \
               xp.Sum(c2[jj]*y[jj] for jj in range(n2)) ,                      \
               sense=xp.minimize)

# 解该问题
p.solve()

# 检查当前状态
if p.getProbStatus() != xp.mip_optimal:
    raise RuntimeError('Problem could not be solved to MIP optimality')

# 获得解，第一阶段的变量，第二阶段的变量，二季短的目标
yopt = p.getSolution(y)
print("The optimal objective is:", p.getObjVal())
print("The first stage variables are:", p.getSolution(x))
print("The second stage variables are:", yopt)
print("The objective of the second stage is:",                                 \
       sum(c2[jj]*yopt[jj] for jj in range(n2)))

# 子问题求解
def subproblem(xhat):

    # 初始化问题
    r=xp.problem()

    # 定义变量
    y=[xp.var() for i in range(n2)]
    z=[xp.var(lb=-xp.infinity) for i in range(n1)]
    epsilon=xp.var(lb=-xp.infinity)
    r.addVariable(y,z,epsilon)

    # 定义约束
    dummy1= [z[i]==xhat[i] for i in range(n1)]
    dummy2= epsilon==1
    constr=[xp.Sum(A1[ii][jj]*z[jj] for jj in range(n1)) +                     \
            xp.Sum(A2[ii][jj]*y[jj] for jj in range(n2))                       \
            - epsilon*b[ii]<=0 for ii in range(m)]
    r.addConstraint(constr,dummy1,dummy2)

    # 定义目标函数
    r.setObjective(xp.Sum(c2[jj]*y[jj] for jj in range(n2)), sense=xp.minimize)
    r.setControl({"presolve":0})

    # 解该问题
    r.setControl ('outputlog', 0)
    r.solve()

    # 寻找切片
    xind1=[r.getIndex(dummy1[ii]) for ii in range(n1)]

    # 根据自问题的解的情况判断下一步
    if r.getProbStatus()==xp.lp_optimal:
        # 获得了最优解
        print("Optimal Subproblem")
        dualmult=r.getDual()
        lamb=[dualmult[ii] for ii in xind1]
        beta=r.getObjVal()
        return(lamb,beta,'Optimal')
    elif r.getProbStatus()==xp.lp_infeas:
        # 子问题不可行
        print("Infeasible Subproblem")
        if not r.hasdualray ():
            print ("Could not retrieve a dual ray, return no good cut instead:")
            xhatones=set(ii for ii in range(n1) if xhat[ii]>=0.5)
            lamb=[2*xhat[ii]-1 for ii in range(n1)]
            beta=-sum(xhat)+1
        else:
            # Extract the dual ray
            dray = []
            r.getdualray (dray)
            print ("Dual Ray:", dray)
            lamb=[dray[ii] for ii in xind1]
            beta=dray[r.getIndex(dummy2)]
        return(lamb,beta,'Infeasible')
    else:
        print("ERROR: Subproblem not optimal or infeasible. Terminating.")
        sys.exit()

# 整数回收函数
def integer_callback(p, data, isheuristic, cutoff):

    print("Entering Integer Callback.")
    if isheuristic ==0:
        print("Integer solution from optimal node relaxation.")
        print("Solution accepted. Cutoff:", cutoff)
        return(False,None)
    else:
        print("Integer solution found from heuristic. Checking subproblem.")
        s=[]
        p.getlpsol(s,None,None,None) # This will load the solution to array s

        # Obtain indices of x and theta in the original problem
        xind=[p.getIndex(x[ii]) for ii in range(n1)]
        thetaind=[p.getIndex(theta)]

        # Construct xhat and thetahat based on the vector s where the full
        # solution was stored and the variable indices
        xhat=[s[ii] for ii in xind]
        thetahat=s[thetaind[0]]
        print("Solution tested x=",xhat, "and theta=",thetahat)
        print("Cutoff is:",cutoff)

        # Solve the subproblem
        (dual_mult,opt,status)=subproblem(xhat)

        if status=='Infeasible':
            # In the case of an infeasible subproblem, simply reject the solution found
            return (True,None)
        elif status=='Optimal':
            if thetahat>=opt-ObjAbsAccuracy:
                # In this case the vector (xhat,thetahat) is feasible, so accept
                # it and accept the cutoff
                print("Accepting pair x=",xhat,",theta=",thetahat )
                print("Accept new cutoff:",cutoff)
                return(False,None)
            else:
                # In this case the solution (xhat,thetahat) is infeasible so
                # reject it
                return (True,None)
        else:
            print("We shouldn't reach this point.")
            print("Rejecting pair x=",xhat,",theta=",thetahat )
            return(True,None)

# 点的回收函数
def node_callback(p, data):

    print("We entered a node callback")

    # Obtain node relaxation solution
    s=[]
    p.getlpsol(s,None,None,None)
    xind=[p.getIndex(x[ii]) for ii in range(n1)]
    thetaind=[p.getIndex(theta)]
    xhat=[s[ii] for ii in xind]
    thetahat=s[thetaind[0]]
    print("Solution tested x=",xhat, "and theta=",thetahat)

    # 开始解子问题
    (dual_mult,opt,status)=subproblem(xhat)
    if status=='Infeasible':
        # 创建feasibility cut
        coefficients=dual_mult
        rhs=-opt
        print("Add cut. Cut stats:")
        print("coefficients:",coefficients)
        print("<=rhs:",rhs)
        print("column indices:",xind)
        # Add the cut (this will reject the point)
        p.addcuts([1],['L'],[rhs],[0,len(xhat)],xind,coefficients)
        print("Rejecting pair x=",xhat,",theta=",thetahat, "with a cut." )
        return 0
    elif status=='Optimal':
        if thetahat>=opt-ObjAbsAccuracy:
            # In this case the vector (xhat,thetahat) is feasible, so accept
            print("Accepting pair x=",xhat,",theta=",thetahat )
            print("An integer callback will be triggered for that pair later.")
            return 0
        else:
            # In this case the solution (xhat,thetahat) is infeasible so reject
            # it and add an optimality cut
            coefficients=[1]+[-dual_mult[ii] for ii in range(len(dual_mult))]
            rhs=opt-sum(dual_mult[ii]*xhat[ii] for ii in range(len(dual_mult)))
            print("Store cut. Cut stats:")
            print("coefficients:",coefficients)
            print(">=rhs:",rhs)
            print("column indices:",thetaind+xind)
            # Add the cut (this will reject the point)
            p.addcuts([1],['G'],[rhs],[0,len(xhat)+1],thetaind+xind,coefficients)
            print("Rejecting pair x=",xhat,",theta=",thetahat,"with a cut." )
            return 0
    else:
        print("ERROR: Subproblem not optimal or infeasible. Terminating.")
        sys.exit()


# 定义Master Problem
p=xp.problem()

# 定义第一阶段变量
x=[xp.var(vartype=xp.binary) for i in range(n1)]

# 修改Lower Bound
theta=xp.var()
p.addVariable(x,theta)

# 定义目标函数
p.setObjective(xp.Sum(c1[jj]*x[jj] for jj in range(n1)) +  theta               \
               ,sense=xp.minimize)

# Declares a user integer solution callback function, called when an 
# integer solution is found by heuristics or during the branch and bound 
# search, but before it is accepted by the Optimizer. This callback 
# function will be called in addition to any integer solution callbacks 
# already added by addcbpreintsol.
p.addcbpreintsol (integer_callback, None, 0)

# Declares an optimal node callback function, called during the branch and 
# bound search, after the LP relaxation has been solved for the current 
# node, and after any internal cuts and heuristics have been applied, but 
# before the Optimizer checks if the current node should be branched. This 
# callback function will be called in addition to any callbacks already 
# added by addcboptnode.
p.addcboptnode (node_callback, None, 0)

p.setControl({"presolve":0,"mippresolve":0,"symmetry":0})

# 解Master problem
p.solve()

if p.getProbStatus() == xp.lp_optimal:
    print("The optimal objective is:",p.getObjVal())
    print("The first stage variables are:",p.getSolution(x))
else:
    print("Could not solve the problem")