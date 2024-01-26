#%%
import graphix_perceval
import perceval as pcvl
# %%
from main import *
# %%

circdepth = 5
depth = 3
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


circuit2 = Circuit(depth)
# alpha = np.random.rand(depth)*2*np.pi
print(alpha)
for j in range(circdepth):
    for i in range(depth):
        circuit2.ry(i,alpha[i])
    for i in range(depth):
        circuit2.rz(i,alpha[i])
    for i in range(depth-1):
        circuit2.cnot(i,i+1)
pattern2 = circuit2.transpile()
pattern2.parallelize_pattern()
#
pattern2.print_pattern()
pattern2.standardize()
pattern2.shift_signals()
pattern2.perform_pauli_measurements()
pattern2.minimize_space()
pattern2.draw_graph()
# out_state2 = pattern2.simulate_pattern(backend="statevector")
# print("overlap of states: ", np.abs(np.dot(out_state.psi.flatten().conjugate(), out_state2.psi.flatten())))
# print("without abs",np.dot(out_state.psi.flatten().conjugate(), out_state2.psi.flatten()))
# print("out state 1\n",out_state)
# print("out state 2\n",out_state2)
print("pattern 1 space:",pattern.max_space(), "pattern 1 layers:", pattern.get_layers())
print("pattern 2 space:", pattern2.max_space(),"pattern 2 layers:", pattern2.get_layers())
#%%
out_state = pattern.simulate_pattern(backend="statevector")
print(out_state)
#%%
pattern.perform_pauli_measurements()
pattern.draw_graph()
out_state2 = pattern.simulate_pattern(backend="statevector")
print(out_state2)
print("overlap of states: ", np.abs(np.dot(out_state.psi.flatten().conjugate(), out_state2.psi.flatten())))
# %%
from graphix_perceval import to_perceval
# %%
pcirc = to_perceval(pattern2)
# %%
print(pcirc)
# %%
print("The circuit is :")
pcvl.pdisplay(pcirc.circ)
# %%
pcirc.set_local_processor("Naive",name="Local processor")
# %%
res = pcirc.get_probability_distribution()
print(res)
# %%
