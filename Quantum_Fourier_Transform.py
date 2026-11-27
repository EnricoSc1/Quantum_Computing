# Generated from: Quantum_Fourier_Transform.ipynb
# Converted at: 2026-11-27T18:25:36.752Z
# Next step (optional): refactor into modules & generate tests with RunCell
# Quick start: pip install runcell

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, Operator

def build_circuity(ket, measure = False):
    
    state = [i for i in ket]
    n = len(state)
    
    if measure == True:
        qc = QuantumCircuit(n, n)
    else:
        qc = QuantumCircuit(n)

    for i in range(n):
        if state[i] == '1':
            qc.x((n - 1) - i)
            
    return n, qc


def quantum_fourier_transform(qc, n_qbs):

    for i in reversed(range(n_qbs)):
        
        qc.h(i)
        
        for j in reversed(range(1, i + 1)):
            
            qc.cp(np.pi/(2 ** j), i, i - j)

    for i in range(int( n_qbs // 2)):
        qc.swap(i, n_qbs - 1 - i)
        
    return qc

start = input('Enter the desired starting state (single ket only): ')

n, qc = build_circuity(start)
quantum_fourier_transform(qc, n)
qc.draw()

Statevector(qc).draw('latex')
