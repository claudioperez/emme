"""
Lower Bound - 2r
================

(220_HW12_P2r)

"""

import ema as em
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
# %config InlineBackend.figure_format = 'svg'

#Remove
mdl = em.rModel(2,3)
n = mdl.dnodes
e = mdl.delems

mdl.node('1', 0.0, 0.0)
mdl.node('2', 8.0, 0.0)
mdl.node('3', 8.0, 6.0)
mdl.node('4', 16., 6.0)
mdl.node('5', 16., -4.)

# elements
mdl.beam('a', n['1'], n['2'])
mdl.beam('b', n['2'], n['3'])
mdl.beam('c', n['3'], n['4'])
mdl.beam('d', n['4'], n['5'])
mdl.truss('e', n['2'], n['4'])

# redundants
mdl.redundant(e['a'], '2')
mdl.redundant(e['c'], '2')
mdl.redundant(e['d'], '3')
mdl.redundant(e['e'], '1')

# Fixities
mdl.fix(n['1'], ['x', 'y', 'rz'])
mdl.fix(n['5'], ['x', 'y', 'rz'])

# Loading
n['3'].p['y'] = -30
n['3'].p['x'] =  50

# Define plastic capacity
e['a'].Qp['+']['2'] = e['a'].Qp['-']['2'] = 120
e['a'].Qp['+']['3'] = e['a'].Qp['-']['3'] = 120
e['c'].Qp['+']['2'] = e['c'].Qp['-']['2'] = 120
e['c'].Qp['+']['3'] = e['c'].Qp['-']['3'] = 120
e['b'].Qp['+']['2'] = e['b'].Qp['-']['2'] = 150
e['b'].Qp['+']['3'] = e['b'].Qp['-']['3'] = 150
e['d'].Qp['+']['2'] = e['d'].Qp['-']['2'] = 180
e['d'].Qp['+']['3'] = e['d'].Qp['-']['3'] = 180
e['e'].Qp['+']['1'] = e['e'].Qp['-']['1'] =  30

mdl.DOF = [[6, 7, 8], [6, 1, 2], [3, 1, 4], [3, 9, 5], [10, 9, 11]]
em.analysis.characterize(mdl)

fig, ax = plt.subplots(1,1)
em.plot_structure(mdl, ax)

B = em.B_matrix(mdl)
A = em.A_matrix(mdl)
P = em.P_vector(B)
B

A.f

Qpr = B.bari@P.f

A_mp = A.o@np.array([1, 1/8, -3/4, 1/8, 3/40])
A_mp

em.analysis.PlasticAnalysis_wLBT(mdl)

Qpl = em.Qpl_vector(mdl)
np.abs(A_mp.T)@Qpl[:,0]

np.abs(np.array([1, 1/8, -3/4, 1/8, 3/40]).T)@np.abs(P.f)

np.array([1, 1/8, -3/4, 1/8, 3/40]).T@P.f

