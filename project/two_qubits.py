from qiskit import QuantumCircuit
from qiskit.quantum_info import DensityMatrix
from qiskit_ibm_runtime import QiskitRuntimeService
import numpy as np
import qiskit
import matplotlib.pyplot as plt
from qiskit_aer.noise import NoiseModel, amplitude_damping_error
from qiskit_aer import QasmSimulator
from qiskit_experiments.library import StateTomography
from qiskit_experiments.library.tomography.fitters import tomography_fitter_data
from qiskit.visualization import array_to_latex
from qiskit.quantum_info import concurrence, DensityMatrix
service = QiskitRuntimeService(
    channel="ibm_quantum", token="3b39233787ff7fa1033c1d5f397a37b92e0c7e601c26a33ba31139a342332405e8102147474c36b5cc675b319d36a4fcda04680d0cda72f02583dc5dcf74ca7e")


dephasing_rate = 0.05
time_steps = np.linspace(0, 1, 5)

qc = QuantumCircuit(2)
qc.h(0)  # Hadamard gate on the first qubit
qc.cx(0, 1)  # CNOT gate to entangle the qubits
for t in time_steps:
    # Modify the circuit to include noise
    noisy_qc = qc.copy()
    noisy_qc(qubit=0, p=dephasing_rate * t)
    noisy_qc.depolarize(qubit=1, p=dephasing_rate * t)

st_circuits = StateTomography(circuit=noisy_qc)
backend = service.backend("ibmq_qasm_simulator")
stdata = st_circuits.run(backend).block_for_results()
state_result = stdata.analysis_results("state")
current_concurrence = concurrence(DensityMatrix(state_result.value))
concurrences = []
concurrences.append(current_concurrence)
plt.figure(figsize=(10, 6))
plt.plot(time_steps, concurrences, 'o-',
         color='b', label='Concurrence vs Time')
plt.title('Decay of Concurrence due to Collective Dephasing')
plt.xlabel('Time')
plt.ylabel('Concurrence')
plt.legend()
plt.grid(True)
plt.show()
