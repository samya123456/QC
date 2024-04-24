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


# Parameters for the experiment
gamma = 0.05  # Amplitude damping rate
time_steps = np.linspace(0, 1, 10)  # Time intervals for applying the noise


qc = QuantumCircuit(1)
qc.x(0)  # Apply X gate to prepare qubit in |1⟩ state


st_circuits = StateTomography(qc)
backend = service.backend("ibmq_qasm_simulator")

noise_model = NoiseModel.from_backend(backend)
for t in time_steps:
    # Amplitude damping error with increasing effect
    ad_error = amplitude_damping_error(gamma * t, excited_state_population=1)
    noise_model.add_quantum_error(ad_error, ['x', 'id'], [0])

backend_qasm = QasmSimulator(method='density_matrix',
                             noise_model=noise_model,
                             )

stdata = st_circuits.run(backend, seed_simulation=100).block_for_results()
# print("stdata = ", stdata)

state_result = stdata.analysis_results("state")
prob = DensityMatrix(state_result.value)
density_matrices = [prob]
probabilities = [dm.data[1, 1].real for dm in density_matrices]


print("prob = ", probabilities)
