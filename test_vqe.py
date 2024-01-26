#%%
from main import *
from graphix_ibmq.runner import IBMQBackend
import qiskit.quantum_info as qi
import matplotlib.pyplot as plt
# %%
circdepth = 5
depth = 2
circuit = Circuit(depth)
alpha = np.random.rand(depth)*2*np.pi
print(alpha)
# for j in range(circdepth):
#     for i in range(depth):
#         circuit.ry(i,alpha[i])
#     for i in range(depth):
#         circuit.rz(i,alpha[i])
#     for i in range(depth-1):
#         circuit.cnot(i,i+1)
circuit.h(0)
circuit.h(1)
# circuit.x(0)
# circuit.x(1)
# circuit.h(2)
# circuit.h(3)
pattern = circuit.transpile()
# pattern.parallelize_pattern()
#
pattern.print_pattern()
pattern.standardize()
pattern.shift_signals()
# pattern.perform_pauli_measurements()
pattern.minimize_space()
# %%
out_state = pattern.simulate_pattern(backend="statevector")
print(out_state.flatten())
# %%
print(np.shape(Ops_j.x))
# %%
import torch
ddimx = np.tensordot(np.eye(2),np.eye(2),axes=0)
print(ddimx[0])
print(ddimx[1])

# %%
print(np.reshape(ddimx,(4,4),'A'))
# %%
import qiskit.quantum_info as qi
pauliI = "XI"
paulimat = qi.Pauli(pauliI)
# print(paulimat.to_matrix())

matI = paulimat.to_matrix()
dot = np.dot(matI,out_state.psi.flatten())
print("psi",out_state.psi.flatten())
print("dot",dot)
overlap = np.dot(out_state.psi.flatten().conjugate(),dot)
print(overlap)
# %%
