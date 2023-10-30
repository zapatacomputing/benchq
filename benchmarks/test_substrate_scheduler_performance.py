import networkx as nx
import pytest

from benchq.resource_estimation.graph_estimator import substrate_scheduler


@pytest.mark.parametrize("preset", ["fast", "optimized"])
class TestSubstrateScheduler:
    @pytest.mark.parametrize(
        "graph",
        [nx.path_graph, nx.complete_graph, nx.star_graph, nx.wheel_graph],
    )
    @pytest.mark.parametrize("size", [10, 100, 1000])
    def test_substrate_scheduler_timing(self, benchmark, graph, size, preset):
        graph = graph(size)
        benchmark(substrate_scheduler, graph, preset)

    @pytest.mark.parametrize(
        "graph",
        [nx.path_graph, nx.complete_graph, nx.star_graph, nx.wheel_graph],
    )
    @pytest.mark.parametrize("size", [10, 100, 1000])
    def test_substrate_scheduler_timing_with_pre_mapping_optimizer(
        self, benchmark, graph, size, preset
    ):
        graph = graph(size)
        benchmark(substrate_scheduler, graph, preset)

    @pytest.mark.parametrize("chain_size", [10, 100])
    @pytest.mark.parametrize("bell_size", [10, 100])
    def test_substrate_scheduler_timing_barbell_graph(
        self, benchmark, chain_size, bell_size, preset
    ):
        graph = nx.barbell_graph(chain_size, bell_size)
        benchmark(substrate_scheduler, graph, preset)

    @pytest.mark.parametrize("size", [10, 100])
    @pytest.mark.parametrize("probablity_of_edge", [0.01, 0.1])
    def test_substrate_scheduler_timing_erdos_renyi(
        self, benchmark, size, probablity_of_edge, preset
    ):
        graph = nx.erdos_renyi_graph(size, probablity_of_edge, seed=123)
        benchmark(substrate_scheduler, graph, preset)
