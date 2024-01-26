#%%
from main import *
from graphix_ibmq.runner import IBMQBackend
import qiskit.quantum_info as qi
import matplotlib.pyplot as plt
# %%
circdepth = 5
depth = 4
circuit = Circuit(depth)
alpha = np.random.rand(depth)*2*np.pi
print(alpha)
for j in range(circdepth):
    for i in range(depth):
        circuit.ry(i,alpha[i])
    for i in range(depth):
        circuit.rz(i,alpha[i])
    for i in range(depth-1):
        circuit.cnot(i,i+1)
pattern = circuit.transpile()
# pattern.parallelize_pattern()
#
pattern.print_pattern()
pattern.standardize()
pattern.shift_signals()
# pattern.perform_pauli_measurements()
pattern.minimize_space()
pattern.draw_graph()
# out_state = pattern.simulate_pattern(backend="statevector")
backend = IBMQBackend(pattern)
backend.to_qiskit()
print(type(backend.circ))

#set the rondom input state
psi = []
for i in range(depth):
    psi.append(qi.random_statevector(2, seed=100+i))
backend.set_input(psi)
# %%
backend.circ.decompose().draw("mpl", style="iqp")
# %%
