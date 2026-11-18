# Generated from: Grover_3qbit.ipynb
# Converted at: 2026-11-18T15:10:24.483Z
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
        qc.x(2)
        qc.ccz(0,1,2)
        qc.x(2)

    if selection == '101':
        qc.x(1)
        qc.ccz(0,1,2)
        qc.x(1)

    if selection == '010':
        qc.x([0,2])
        qc.ccz(0,1,2)
        qc.x([0,2])

    if selection == '110':
        qc.x(0)
        qc.ccz(0,1,2)
        qc.x(0)

    if selection == '001':
        qc.x([1,2])
        qc.ccz(0,1,2)
        qc.x([1,2])

def oracle2(sel, n_bits):

    CnZ = Operator.from_label('I' * n_bits) - Operator.from_label('I' + '1' * (n_bits - 1)) + Operator.from_label('Z' + '1' * (n_bits - 1))
    
    for i, bit in enumerate(sel[::-1]):
        if bit == '0': qc.x(i)

    # For n qbits and n-1 control bits we define CnZ = id ^T n - id ^ |1><1| ^T (n-1) + Z ^ |1><1| ^T (n-1)
    qc.unitary(CnZ, [i for i in range(len(sel))], label = 'CnZ')

    for i, bit in enumerate(sel[::-1]):
        if bit == '0': qc.x(i)

n = 4
qc = QuantumCircuit(n,n)
qc.h(range(n))
superposition_state = Statevector(qc) 

selection = '1110'

identity = Operator.from_label(n * 'I')
projector = Statevector.to_operator(superposition_state)
diffusion = - 2 * projector + identity

for _ in range(3):
    oracle2(selection, 4)
    qc.unitary(diffusion, [i for i in list(range(n))], label = 'diffusion')

qc.measure(range(n), range(n))
qc.draw()

aer = AerSimulator()
job = aer.run(qc, shots = 1000)
result = job.result()
counts = result.get_counts()

plot_histogram(counts)
