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
    synthesized: bool

    @property
    def n_nodes(self) -> int:
        n_nodes = sum(
            len(graph) * multiplicity
            for graph, multiplicity in zip(self.subgraphs, self.program.multiplicities)
        )
        # account for double counting of data qubits coming from each graph
        return n_nodes - self.program.num_data_qubits * (
            len(self.program.subroutine_sequence) - 1
        )
