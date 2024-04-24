from qiskit_ibm_runtime.fake_provider import FakeManila
from qiskit import QuantumCircuit
from qiskit_aer.noise import NoiseModel
# load necessary Runtime libraries
from qiskit.circuit import Parameter
from qiskit_ibm_runtime import QiskitRuntimeService, Sampler, Estimator, Session, Options
import numpy as np
import matplotlib.pyplot as plt
service = QiskitRuntimeService(
    channel="ibm_quantum", token="3b39233787ff7fa1033c1d5f397a37b92e0c7e601c26a33ba31139a342332405e8102147474c36b5cc675b319d36a4fcda04680d0cda72f02583dc5dcf74ca7e"
)
# Make a noise model
fake_backend = FakeManila()
noise_model = NoiseModel.from_backend(fake_backend)

# Set options to include the noise model
options = Options()
options.simulator = {
    "noise_model": noise_model,
    "basis_gates": fake_backend.configuration().basis_gates,
    "coupling_map": fake_backend.configuration().coupling_map,
    "seed_simulator": 42
}

# Set number of shots, optimization_level and resilience_level
options.execution.shots = 1000
options.optimization_level = 0
options.resilience_level = 0
# Set options to include the noise model with error mitigation
options_with_em = Options()
options_with_em.simulator = {
    "noise_model": noise_model,
    "basis_gates": fake_backend.configuration().basis_gates,
    "coupling_map": fake_backend.configuration().coupling_map,
    "seed_simulator": 42
}
theta = Parameter('theta')
qc = QuantumCircuit(2, 1)
qc.x(1)
qc.h(0)
qc.cp(theta, 0, 1)
qc.h(0)
qc.measure(0, 0)
# Set number of shots, optimization_level and resilience_level
options_with_em.execution.shots = 1000
options_with_em.optimization_level = 0  # no optimization
options_with_em.resilience_level = 1  # M3 for Sampler and T-REx for Estimator
backend = "ibmq_qasm_simulator"
phases = np.linspace(0, 2*np.pi, 50)
individual_phases = [[phase] for phase in phases]
with Session(service=service, backend=backend):
    # include the noise model without M3
    sampler = Sampler(options=options, backend=backend)
    job = sampler.run(
        circuits=[qc]*len(phases),
        parameter_values=individual_phases
    )
    result = job.result()
    prob_values = [1-dist[0] for dist in result.quasi_dists]

    # include the noise model with M3

sampler = Sampler(options=options_with_em, backend=backend)
job = sampler.run(
    circuits=[qc]*len(phases),
    parameter_values=individual_phases
)
result = job.result()
prob_values_with_em = [1-dist[0] for dist in result.quasi_dists]


plt.plot(phases, prob_values, 'o', label='Noisy')
plt.plot(phases, prob_values_with_em, 'o', label='Mitigated')
plt.plot(phases, np.sin(phases/2,)**2, label='Theory')
plt.xlabel('Phase')
plt.ylabel('Probability')
plt.legend()
plt.grid(True)
plt.show()


# https://docs.quantum.ibm.com/verify/using-ibm-quantum-simulators
