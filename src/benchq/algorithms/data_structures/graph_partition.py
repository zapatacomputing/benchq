from dataclasses import dataclass
from typing import List, Union

import networkx as nx
from cirq.circuits.circuit import Circuit as CirqCircuit
from orquestra.quantum.circuits import Circuit as OrquestraCircuit
from qiskit.circuit import QuantumCircuit as QiskitCircuit

from ...problem_embeddings.quantum_program import QuantumProgram

AnyCircuit = Union[OrquestraCircuit, CirqCircuit, QiskitCircuit]


@dataclass
class GraphPartition:
    program: QuantumProgram
    subgraphs: List[nx.Graph]

    @property
    def n_nodes(self) -> int:
        n_nodes = 0
        for subgraph in self.subgraphs:
            n_nodes += subgraph.number_of_nodes()
        return n_nodes

    @property
    def n_t_gates(self) -> int:
        return self.program.n_t_gates

    @property
    def n_rotation_gates(self) -> int:
        return self.program.n_rotation_gates
