from dataclasses import dataclass
from typing import List, Union

import networkx as nx
from cirq.circuits.circuit import Circuit as CirqCircuit
from orquestra.quantum.circuits import Circuit as OrquestraCircuit
from qiskit.circuit import QuantumCircuit as QiskitCircuit

from ...data_structures import QuantumProgram

AnyCircuit = Union[OrquestraCircuit, CirqCircuit, QiskitCircuit]


@dataclass
class GraphPartition:
    program: QuantumProgram
    subgraphs: List[nx.Graph]
    delayed_gate_synthesis: bool

    @property
    def n_nodes(self) -> int:
        return self.program.n_nodes

    @property
    def n_t_gates(self) -> int:
        return self.program.n_t_gates

    @property
    def n_rotation_gates(self) -> int:
        return self.program.n_rotation_gates
