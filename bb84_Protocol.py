# Generated from: bb84_Protocol.ipynb
# Converted at: 2026-11-16T15:38:16.132Z
# Next step (optional): refactor into modules & generate tests with RunCell
# Quick start: pip install runcell

from qiskit.quantum_info import Statevector
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import numpy as np

n_bits = 4
basis_1 = np.random.randint(2, size = n_bits)
random_key = np.random.randint(2, size = n_bits)
basis_2 = np.random.randint(2, size = n_bits)
print(basis_1, random_key, basis_2)

qc = QuantumCircuit(n_bits, n_bits)

for i in range(n_bits):
    if random_key[i] == 1:
        qc.x(i)
    if basis_1[i] == 1:
        qc.h(i)

for i in range(n_bits):
    if basis_2[i] == 1:
        qc.h(i)

qc.draw()

qc.measure(range(n_bits), range(n_bits))
qc.draw()

aer = AerSimulator()
job = aer.run(qc, shots = 1)
result = job.result()
counts = list(result.get_counts().keys())[0][::-1]
received_key = np.array([int(bit) for bit in counts])

print(received_key)

keep = basis_1 == basis_2

bits_1 = basis_1[keep].tolist()
bits_2 = basis_2[keep].tolist()

print(bits_1, bits_2)

if random_key[keep].tolist() == received_key[keep].tolist():
    print ('Matched keys!')
    print(received_key[keep].tolist())