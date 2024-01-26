#%%
from main import *
#%%
# apply H gate to a qubit in + state

circuit = Circuit_j(1)
circuit.y_j(0)
circuit.h_j(0)
circuit.z_j(0)
pattern = circuit.transpile_j()
# %%
pattern.print_pattern()
# %%
pattern.draw_graph()
# %%
out_state = pattern.simulate_pattern(backend="statevector")
print(out_state)
# %%
# apply H gate to a qubit in + state

circuit2 = Circuit(1)
circuit2.y(0)
circuit2.h(0)
circuit2.z(0)
pattern2 = circuit2.transpile()
# %%
pattern2.print_pattern()
# %%
pattern2.draw_graph()
# %%
out_state2 = pattern2.simulate_pattern(backend="statevector")
print(out_state2)
# %%
print("overlap of states: ", np.abs(np.dot(out_state2.psi.flatten().conjugate(), out_state.psi.flatten())))
# %%
print(out_state2.psi)
print(out_state.psi *1j)

# %%
circuit = Circuit_j(2)
circuit.cz(0,1)
pattern = circuit.transpile_j()
# %%
pattern.print_pattern()
# %%
pattern.draw_graph()
# %%
out_state = pattern.simulate_pattern(backend="statevector")
print(out_state)
# %%
# Test using Elham's paper with all angles set to 0:
circuit = Circuit_j(3)

# 1st layer entangle 0-2
circuit.cz(0,2)
# 2nd layer add J0(0) + entangle 1-2
circuit.j(0,0)
circuit.cz(1,2)
# 3rd layer entangle 0-2
circuit.cz(0,2)
# 4th layer J1(0)
circuit.j(1,0)
# 5the layer J2(0)
circuit.j(1,0)
pattern = circuit.transpile_j()
# pattern.parallelize_pattern()
#
pattern.print_pattern()

pattern.draw_graph()

# out_state = pattern.simulate_pattern(backend="statevector")
# print(out_state)
# pattern.parallelize_pattern()
# out_state = pattern.simulate_pattern(backend="statevector")
# print(out_state)
#%%
width = 6
nodes = [j for j in range(width)]
input_nodes = [0,2,3]
output_nodes = [1,2,5]
# All nodes are output nodes at first to be removed from list at the end of measurement
pat = Pattern(input_nodes = input_nodes,output_nodes = nodes,width=width)

seq = [["E",(0,1)],
       ["E",(0,2)],
       ["E",(1,2)],
       ["E",(2,3)],
       ["E",(3,4)],
       ["E",(4,5)],
       ["M", 0, "XY", 0, [], []],
       ["X", 1, [0]],
       ["M", 3, "XY", 0, [], []],
       ["X", 4, [3]],
       ["M", 4, "XY", 0, [], []],
       ["X", 5, [4]],
       ]
for cmd in seq:
    pat.add(cmd)
pat.print_pattern()
# pat.standardize_and_shift_signals()
pat.draw_graph()

out_pat = pat.simulate_pattern(backend="statevector")
#%%
print(out_state)
print(out_pat)
# out_state = pattern.simulate_pattern(backend="statevector")
# print(out_state)
# out_pat = pat.simulate_pattern(backend="statevector")
# print(out_pat)

# %%
print("overlap of states: ", np.abs(np.dot(out_state.psi.flatten().conjugate(), out_pat.psi.flatten())))
# %%
print(out_state.psi.flatten())
print(out_pat.psi.flatten())
# %%
out_trans = np.transpose(out_state.psi,(0,2,1))
print(out_trans)
# %%
print("overlap of states: ", np.abs(np.dot(out_trans.flatten().conjugate(), out_pat.psi.flatten())))
# %%
from graphix import Statevec
state = Statevec(nqubit=3,plus_states=True)
state.evolve(Ops_j.cz,[0,2])
state.evolve_single(Ops_j.h,0)
state.evolve(Ops_j.cz,[1,2])
state.evolve(Ops_j.cz,[0,2])
state.evolve_single(Ops_j.h,1)
state.evolve_single(Ops_j.h,1)
print(state.psi)
# %%
print("overlap of states: ", np.abs(np.dot(out_pat.psi.flatten().conjugate(), state.psi.flatten())))

# %%
pat.print_pattern()
print()
print()
pattern.print_pattern()
# %%
#%%
width = 6
nodes = [j for j in range(width)]
input_nodes = [0,3,2]
output_nodes = [2,5,1]
# All nodes are output nodes at first to be removed from list at the end of measurement
pat = Pattern()

# init
for node in input_nodes:
    pat.add(["N",node])
pat.set_input_nodes(input_nodes)

pat.add(["E",(0,2)])

pat.add(["N",1])
pat.add(["E",(0,1)])
pat.add(["M", 0, "XY", 0, [], []])
pat.add(["X", 1, [0]])
pat.add(["E",(3,2)])
pat.add(["E",(2,1)])
pat.add(["N",4])
pat.add(["E",(3,4)])
pat.add(["M", 3, "XY", 0, [], []])
pat.add(["X", 4, [3]])
pat.add(["N",5])
pat.add(["E",(4,5)])
pat.add(["M", 4, "XY", 0, [], []])
pat.add(["X", 5, [4]])

pat.set_output_nodes(output_nodes)

seq = [["E",(0,1)],
       ["E",(0,2)],
       ["E",(1,2)],
       ["E",(2,3)],
       ["E",(3,4)],
       ["E",(4,5)],
       ["M", 0, "XY", 0, [], []],
       ["X", 1, [0]],
       ["M", 3, "XY", 0, [], []],
       ["X", 4, [3]],
       ["M", 4, "XY", 0, [], []],
       ["X", 5, [4]],
       ]
# for cmd in seq:
#     pat.add(cmd)
pat.print_pattern()
# pat.standardize_and_shift_signals()
pat.draw_graph()

out_pat = pat.simulate_pattern(backend="statevector")
# %%
print(out_pat.psi)
print(out_state.psi)
# %%
print("overlap of states: ", np.abs(np.dot(out_pat.psi.flatten().conjugate(), state.psi.flatten())))
# %%
