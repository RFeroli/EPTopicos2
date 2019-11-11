from sympy import *

y= symbols('box')
gfg_exp = '1 + 1*box - box'
print(solve(gfg_exp, y))
