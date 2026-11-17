# Generated from: Random_Numbers.ipynb
# Converted at: 2026-11-17T09:28:57.438Z
# Next step (optional): refactor into modules & generate tests with RunCell
# Quick start: pip install runcell

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import numpy as np

n_bits = 20
n_numbers = 10

qc = QuantumCircuit(n_bits, n_bits)
qc.h(range(n_bits))
qc.measure(range(n_bits),range(n_bits))
qc.draw()

aer = AerSimulator()
job = aer.run(qc, shots = n_numbers)
result = job.result()
counts = list(result.get_counts().keys())

random_numbers = [int(b,2) for b in counts]

print(random_numbers)
