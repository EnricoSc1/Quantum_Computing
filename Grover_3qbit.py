# Generated from: Grover_3qbit.ipynb
# Converted at: 2026-11-18T09:34:07.413Z
# Next step (optional): refactor into modules & generate tests with RunCell
# Quick start: pip install runcell

import numpy as np
from qiskit.quantum_info import Statevector, Operator
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

def oracle(selection):

    if selection == '111':
        qc.ccz(0,1,2)

    if selection == '000':
        qc.x([0,1,2])
        qc.ccz(0,1,2)
        qc.x([0,1,2])

    if selection == '100':
        qc.x([0,1])
        qc.ccz(0,1,2)
        qc.x([0,1])

    if selection == '011':
        qc.cz(0,1)
        qc.ccz(0,1,2)

    if selection == '101':
        qc.cz(0,2)
        qc.ccz(0,1,2)

    if selection == '010':
        qc.x([0,2])
        qc.ccz(0,1,2)
        qc.x([0,2])

    if selection == '110':
        qc.cz(1,2)
        qc.ccz(0,1,2)

    if selection == '001':
        qc.x([1,2])
        qc.ccz(0,1,2)
        qc.x([1,2])

qc = QuantumCircuit(n,n)
qc.h(range(n))
superposition_state = Statevector(qc) 


n = 3
selection = '100'

identity = Operator.from_label(n * 'I')
projector = Statevector.to_operator(superposition_state)
diffusion = - 2 * projector + identity

for _ in range(2):
    oracle(selection)
    qc.unitary(diffusion, [0,1,2], label = 'diffusion')

qc.measure(range(n), range(n))
qc.draw()

aer = AerSimulator()
job = aer.run(qc, shots = 1000)
result = job.result()
counts = result.get_counts()

plot_histogram(counts)