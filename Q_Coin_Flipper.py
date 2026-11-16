# Generated from: Q_Coin_Flipper.ipynb
# Converted at: 2026-11-16T10:10:53.704Z
# Next step (optional): refactor into modules & generate tests with RunCell
# Quick start: pip install runcell

import random
choice = input('Heads or tails?')

coin = random.randint(1,2)

if coin == 1:
    result = 'heads'
else:
    result = 'tails'

if result == choice:
    print('You win!')
else:
    print('You lose!')

# Quantum version

from qiskit.quantum_info import Statevector
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

qc = QuantumCircuit(1,1)
qc.h(0)
qc.measure(0,0)
qc.draw()

aer = AerSimulator()
job = aer.run(qc, shots = 1000)
result = job.result().get_counts()

print(result)

plot_histogram(result)

q_choice = input('Heads or tails?')

aer = AerSimulator()
job = aer.run(qc, shots = 1)
result = job.result().get_counts().keys()
q_coin = int(list(result)[0])

if q_coin == 0:
    outcome = 'heads'
else:
    outcome = 'tails'

if outcome == q_choice:
    print('You win!')
else:
    print('You lose!')