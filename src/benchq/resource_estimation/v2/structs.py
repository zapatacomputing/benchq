# When list of subgraphs is passed, it seems it has to be accompanied
# by data_qubits_map_list. Hence, they are actually part of the same data
# structure.
#
# I made it a dataclass because it is simple, but it does not have to be one
from ...data_structures import QuantumProgram
from typing import List
from dataclasses import dataclass
import networkx as nx


@dataclass
class GraphPartition:
    program: QuantumProgram
    subgraphs: List[nx.Graph]
    data_qubits_map_list: List[List[int]]

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
