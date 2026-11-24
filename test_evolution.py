# Generated from: Test_Evolution.ipynb
# Converted at: 2026-11-24T15:50:58.790Z
# Next step (optional): refactor into modules & generate tests with RunCell
# Quick start: pip install runcell

import numpy as np
from qiskit.quantum_info import Operator, Statevector
from qiskit.circuit.library import XGate, RZGate
from qiskit import QuantumCircuit
%matplotlib inline

Xgate = Operator.from_label('X')
identity = Operator.from_label('I')
z_proj = Operator.from_label('0')
o_proj = Operator.from_label('1')
CNOT = (z_proj ^ identity) + (o_proj ^ Xgate)

evolution = []
step = 20

times = np.linspace(0, 10, step)
omega = np.random.rand(step)

for t, o in zip(times, omega):

    phi = o * t
    
    RZ = Operator(RZGate(phi))

    interaction = CNOT @ (RZ ^ identity) @ CNOT
    
    
    qc = QuantumCircuit(2)
    qc.z(1)
    qc.h([0,1])
    qc.cx(0,1)
    qc.unitary(interaction, [0,1])
    qc.h([0,1])
    sv = Statevector(qc)
    probabilities = sv.probabilities()
    evolution.append(probabilities)

arr = np.array(evolution)


plt.plot(times, arr[:, 0], label="P(|00>)")
plt.plot(times, arr[:, 1], label="P(|01>)")
plt.plot(times, arr[:, 2], label="P(|10>)")
plt.plot(times, arr[:, 3], label="P(|11>)")
plt.xlabel("Time (t)")
plt.ylabel("Probability")
plt.legend()
plt.grid(True)
plt.show()
