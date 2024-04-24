# Quantum Teleportation with Qiskit

## Overview

This repository contains Python code implementing Quantum Teleportation using Qiskit, a Python library for quantum computing. Quantum Teleportation is a fundamental protocol in quantum information theory that allows the transfer of quantum states between distant qubits.

## Prerequisites

Before running the code, ensure you have the following installed:

- Python 3.x
- Qiskit
- IBM Quantum Experience account (for running on real quantum hardware)

## Setup

1. Clone the repository:

2. Install the required dependencies:

   
3. Optionally, set up your IBM Quantum Experience account credentials:

```python
from qiskit import IBMQ
IBMQ.save_account('YOUR_API_TOKEN')

python code/teleportation.py
```
pip uninstall qiskit-terra

https://qiskit-extensions.github.io/qiskit-experiments/manuals/verification/state_tomography.html