# Generated from: Q_Teleport_Other_States.ipynb
# Converted at: 2026-11-23T16:57:04.901Z
# Next step (optional): refactor into modules & generate tests with RunCell
# Quick start: pip install runcell

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.result import marginal_counts
from qiskit.quantum_info import Statevector, Operator, state_fidelity, random_statevector
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram, plot_distribution

#This function builds the quantum circuit taking as inputs the following quantities:
#1. The instructions to construct the state that we want to teleport as a callable function.
#2. The possible outcome pair from the measurements of qubit0 and qubit1.
#The output is the quantum circuit itself, which takes into account the required corrections from the measurements.
def build_circuit(prepare_teleport_state, m0, m1):

    qc = QuantumCircuit(3)
    prepare_teleport_state(qc)

    qc.h(1)
    qc.cx(1,2)

    qc.cx(0,1)
    qc.h(0)

    if m1 == 1:
        qc.x(2)

    if m0 == 1:
        qc.z(2)

    return qc

#The following function extract the single qbit2 from the multiparticle state, given by | q2, q1, q0 >.
#As input it takes:
#1. an array describing the superposition of the multiparticle states with each amplitude.
#2. The possible outcome pair from the measurements of qubit0 and qubit1.
#It extracts the amplitude of the | 0 > and | 1 > components, computes the norm and the normalized single-qubit Statevector.
def make_q2(sv_data ,m0 ,m1):

    amp0 = sv_data[m0 + m1 * 2 + 0 * 4]
    amp1 = sv_data[m0 + m1 * 2 + 1 * 4]
    norm = np.sqrt(abs(amp0) ** 2 + abs(amp1) ** 2)

    return Statevector([amp0 / norm, amp1 /norm])

#Build function for the circuit in the specific scenario of a simulator wiht measurements on all 3 qubits
def build_simulation_circuit(prepare_teleport_state):

    qc = QuantumCircuit(3,3)
    prepare_teleport_state(qc)
    
    qc.h(1)
    qc.cx(1,2)
    
    qc.cx(0,1)
    qc.h(0)
    
    qc.measure(0,0)
    qc.measure(1,1)
    
    qc.cx(1,2)
    qc.cz(0,2)
    
    qc.measure(2,2)

    return qc
    

#Dictionary mapping each state label to a nested dictionary with two keys:
#prep: a lambda function that prepares the labelled state on qubit 0.
#ref: the expected reference Statevector used to verify teleportation fidelity.
theta = np.pi/3
phi = np.pi / 4
rand_sv = random_statevector(2)

#The circuit configuration and the corrections are valid for any state vector chosen to teleport, see the examples.
states = {
    '|+>' : { 'prep' : lambda qc : qc.h(0), 'ref' : Statevector([np.sqrt(1/2), np.sqrt(1/2)])},
    '|->' : { 'prep' : lambda qc : (qc.h(0), qc.z(0)), 'ref' : Statevector([np.sqrt(1/2), - np.sqrt(1/2)])},
    'Ry(pi/3)|0⟩' : { 'prep' : lambda qc : qc.ry(theta, 0), 'ref' : Statevector([np.cos(theta/2), np.sin(theta/2)])},
    'random' : { 'prep': lambda qc, s = rand_sv : qc.prepare_state(s, 0), 'ref': rand_sv},
    'U(pi/3, pi/4)|0⟩' : {'prep': lambda qc: qc.u(theta, phi, 0, 0), 'ref': Statevector([np.cos(theta / 2), np.exp(1j * phi) * np.sin(theta / 2)])}
} 

#Hard coding the measurement process using for loops
for name, info in states.items():
    
    fidelities = []
    
    for m0 in [0,1]: #Simulates the measurements on the qubit0
        
        for m1 in [0,1]: #Simulates the measurements on the qubit1
            
            qc = build_circuit(info['prep'], m0, m1)
            sv = Statevector(qc)
            q2 = make_q2(sv.data, m0, m1)
            fidelities.append(state_fidelity(q2, info['ref']))

    avg = np.mean(fidelities)
    print(f'{name} : average fidelity is {avg:.6f}')

#Simulation of the quantum circuit for different states
countings = []
for name, info in states.items():
            
    qcs = build_simulation_circuit(info['prep'])
    aer = AerSimulator()
    t_qcs = transpile(qcs, aer) #Required to include random state vectors by making the circuit compatible with the underlying simulator
    job = aer.run(t_qcs, shots = 1000)
    res = job.result()
    counts = res.get_counts()

    countings.append(counts)

q2_counts = marginal_counts(countings[3], indices = [2]) #Select the subset of countings related to specific subset of qubits

plot_histogram(q2_counts)

plot_distribution(q2_counts) #Plot the normalized histogram
