from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit import QuantumCircuit

service = QiskitRuntimeService(
    channel="ibm_quantum", token="3b39233787ff7fa1033c1d5f397a37b92e0c7e601c26a33ba31139a342332405e8102147474c36b5cc675b319d36a4fcda04680d0cda72f02583dc5dcf74ca7e")


# Create empty circuit
example_circuit = QuantumCircuit(2)
example_circuit.measure_all()

# You'll need to specify the credentials when initializing QiskitRuntimeService, if they were not previously saved.
# service = QiskitRuntimeService()
backend = service.backend("ibmq_qasm_simulator")

sampler = Sampler(backend)
job = sampler.run([example_circuit])
print(f"job id: {job.job_id()}")
result = job.result()
print(result)
