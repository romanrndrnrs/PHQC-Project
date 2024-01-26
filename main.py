#%%
import graphix
from graphix.transpiler import Circuit
from graphix.pattern import Pattern
import cmath
import numpy as np
# %%
class Circuit_j(graphix.transpiler.Circuit):
    def __init__(self, width: int):
        super().__init__(width)
    
    def j(self, qubit: int, alpha: float):
        """
        Parameters
        ----------
        qubit: int
            target qubit
        alpha : float
            rotation angle in radian        
        """
        assert qubit in np.arange(self.width)
        self.instruction.append(["J",qubit,alpha])
    
    def cz(self, control: int, target: int):
        """CZ gate

        Parameters
        ---------
        control : int
            control qubit
        target : int
            target qubit
        """
        assert control in np.arange(self.width)
        assert target in np.arange(self.width)
        assert control != target
        self.instruction.append(["CZ", [control, target]])
    
    def h_j(self, qubit: int):
        """Hadamard gate expressed using J(alpha) and CZ
        H = J(0)

        Parameters
        ---------
        qubit : int
            target qubit
        """
        assert qubit in np.arange(self.width)
        self.j(qubit,0)
    def x_j(self, qubit):
        """Pauli X gate expressed using J(alpha) and CZ
        X = J(pi)J(0)
        Parameters
        ---------
        qubit : int
            target qubit
        """
        assert qubit in np.arange(self.width)
        self.j(qubit,0)
        self.j(qubit,np.pi)

    def z_j(self, qubit: int):
        """Pauli Z gate expressed using J(alpha) and CZ
        Z = J(0)J(pi)
        Parameters
        ---------
        qubit : int
            target qubit
        """
        assert qubit in np.arange(self.width)
        self.j(qubit,np.pi)
        self.j(qubit,0)

    def y_j(self, qubit: int):
        """Pauli Y gate expressed using J(alpha) and CZ
        Y = iZX, we discard the global phase i = e^(i*pi/2) in our circuit because it does not affect probabilities / computations

        Parameters
        ---------
        qubit : int
            target qubit
        """
        assert qubit in np.arange(self.width)
        self.z_j(qubit)
        self.x_j(qubit)
    
    def transpile_j(self):
        """gate-to-MBQC in J(alpha) CZ gate basis transpile function.

        Returns
        --------
        pattern : :class:`graphix.pattern.Pattern` object
        """
        Nnode = self.width
        input = [j for j in range(self.width)]
        out = [j for j in range(self.width)]
        pattern = Pattern(input_nodes=input, width=self.width)
        pattern.seq = [["N", i] for i in input]
        for instr in self.instruction:
            if instr[0] == "J":
                ancilla = Nnode
                out[instr[1]], seq = self._j_command(out[instr[1]],ancilla,instr[2])
                pattern.seq.extend(seq)
                Nnode += 1
            elif instr[0] == "CZ":
                out[instr[1][0]], out[instr[1][1]], seq = self._cz_command(out[instr[1][0]], out[instr[1][1]])
                pattern.seq.extend(seq)
            else:
                raise ValueError("Unknown instruction, commands not added")
        
        pattern.output_nodes = out
        pattern.Nnode = Nnode
        return pattern
    
    @classmethod
    def _j_command(self, input_node: int, ancilla: int, alpha):
        """MBQC commands for J(alpha) gate

        Parameters
        ---------
        input_node : int
            target node on graph
        ancilla : int
            ancilla node index to be added

        Returns
        ---------
        out_node : int
            control node on graph after the gate
        commands : list
            list of MBQC commands
        """
        seq = [["N", ancilla]]
        seq.append(["E", (input_node, ancilla)])
        seq.append(["M", input_node, "XY", (-1 * alpha) / np.pi, [], []])
        seq.append(["X", ancilla, [input_node]])
        return ancilla, seq
    @classmethod
    def _cz_command(self,control_node:int,target_node:int):
        """MBQC commands for J(alpha) gate

        Parameters
        ---------
        input_node : int
            target node on graph
        ancilla : int
            ancilla node index to be added

        Returns
        ---------
        out_node_control : int
            control node on graph after the gate
        out_node_target : int
            target node on graph after the gate
        commands : list
            list of MBQC commands
        """
        seq =  [["E", (control_node, target_node)]]
        return control_node, target_node, seq
#%%
class Ops_j(graphix.ops.Ops):
    @staticmethod
    def j(alpha:float):
        """J(alpha) rotation
        
        Parameters
        ----------
        alpha : float
            rotation angle in radian

        Returns
        ----------
        operator : 2*2 np.array
        """
        return np.array([[1, 1], [cmath.exp(1j * alpha), - cmath.exp(1j * alpha)]]) / np.sqrt(2)
    
