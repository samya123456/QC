from qiskit import QuantumCircuit

# Create a quantum circuit with two qubits
qc = QuantumCircuit(2)

# Initialize qubits in |00⟩ state
qc.initialize([1, 0], 0)
qc.initialize([1, 0], 1)

# Apply Hadamard gate to the first qubit
qc.h(0)

# Apply CNOT gate to entangle the qubits
qc.cx(0, 1)
