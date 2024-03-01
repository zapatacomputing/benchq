from dataclasses import dataclass


@dataclass
class GraphData:
    """Minimal set of graph-related data needed for resource estimation."""

    max_graph_degree: int
    n_nodes: int
    n_t_gates: int
    n_rotation_gates: int
    n_measurement_steps: int
