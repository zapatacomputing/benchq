################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
"""
The current stitching properties of an ASG. This is used to keep track of
whether the ASG can be concatenated with other ASGs or if one can add gates
to the ASG. If takes_input is true, then one can concatenate this ASG after
previous asg. If gives output is true, then one can concatenate an ASG after
this one by connecting the output_nodes.

Attributes:
    takes_graph_input (bool): Whether the ASG can be concatenated after another ASG.
    gives_graph_output (bool): Whether the ASG can be concatenated before another ASG.
    graph_input_nodes (Vector{Qubit}): Nodes which are connected to the output nodes
        of a previous graph in order to make a concatenated graph with this graph
        second and the other graph first. If takes_graph_input is false, graph_input_nodes
        will be an empty vector.
    graph_output_nodes (Vector{Qubit}): Nodes which are connected to the input nodes
        of the next graph in order to make a concatenated graph with this graph
        first and the other graph second. If gives_graph_output is false, output_nodes
        will be an empty vector.
    gate_output_nodes (Vector{Qubit}): Nodes which can be acted upon by the
        GraphSim algorthm. That is, individual gates can act on these nodes,
        but they cannot be used to concatenate graphs. Because of this, if
        gives_graph_output is true, then gate_output_nodes is the last qubits
        that the gates acted on before creating the output nodes.
"""
mutable struct StitchingProperties
    takes_graph_input::Bool
    gives_graph_output::Bool
    graph_input_nodes::Vector{Qubit}
    graph_output_nodes::Vector{Qubit}
    gate_output_nodes::Vector{Qubit}
end
StitchingProperties(takes_graph_input, gives_graph_output, n_qubits) = StitchingProperties(
    takes_graph_input,
    gives_graph_output,
    [],
    [],
    [Qubit(i) for i = 1:n_qubits]
)

function Base.show(io::IO, sp::StitchingProperties)
    decimal_graph_input_nodes = [Int(qubit) for qubit in sp.graph_input_nodes]
    decimal_graph_output_nodes = [Int(qubit) for qubit in sp.graph_output_nodes]
    decimal_gate_output_nodes = [Int(qubit) for qubit in sp.gate_output_nodes]
    print(io, "StitchingProperties(\n    " *
              "takes_graph_input = $(sp.takes_graph_input),\n    " *
              "gives_graph_output = $(sp.gives_graph_output),\n    " *
              "graph_input_nodes = $(decimal_graph_input_nodes),\n    " *
              "graph_output_nodes = $(decimal_graph_output_nodes),\n    " *
              "gate_output_nodes = $(decimal_gate_output_nodes)\n  )"
    )
end

function python_stitching_properties(stitching_properties::StitchingProperties)
    return Dict(
        "takes_graph_input" => stitching_properties.takes_graph_input,
        "gives_graph_output" => stitching_properties.gives_graph_output,
        "graph_input_nodes" => pylist(stitching_properties.graph_input_nodes .- 1),
        "graph_output_nodes" => pylist(stitching_properties.graph_output_nodes .- 1),
        "gate_output_nodes" => pylist(stitching_properties.gate_output_nodes .- 1)
    )
end

"""
Hyperparameters which can be used to speed up the compilation.

Attributes:
    teleportation_threshold::Int      max node degree allowed before state is teleported
    teleportation_distance::Int       number of teleportations to do when state is teleported
    min_neighbor_degree::Int          stop searching for neighbor with low degree if
                                        neighbor has at least this many neighbors
    max_num_neighbors_to_search::Int  max number of neighbors to search through when finding
                                        a neighbor with low degree
    decomposition_strategy::Int       strategy for decomposing non-clifford gate
                                        0: keep current qubit as data qubit
                                        1: teleport data to new qubit which becomes data qubit
"""
struct RbSHyperparams
    teleportation_threshold::UInt16
    teleportation_distance::UInt8
    min_neighbor_degree::UInt8
    max_num_neighbors_to_search::UInt32
    decomposition_strategy::UInt8 # TODO: make pauli tracker work witn decomposition_strategy=1
end

default_hyperparams = RbSHyperparams(40, 4, 6, 1e5, 0)
# Hyperparameter choices which disallow teleportation in the compilation
graphsim_hyperparams(min_neighbor_degree, max_num_neighbors_to_search) = RbSHyperparams(65535, 2, min_neighbor_degree, max_num_neighbors_to_search, 0)
default_graphsim_hyperparams = graphsim_hyperparams(6, 1e5)


"""
Data on the aglortihm specific graph state. During computation, this
struct may contain more nodes than are actually used in the graph state.
At the end of the computation, the data structures are resized to only
contain the nodes which are actually used in the graph state. A lack
of input and output nodes indicate that this graph is not stitchable.

Attributes:
    edge_data (Vector{AdjList}): for each node, this list stores a list of that node's neighbors
    sqs (Vector{UInt8}): single qubit clifford symplectic operations
                            on each node. The symplectic operations are
                            just the clifford operators modulo the paulis
    sqp (Vector{UInt8}): single qubit pauli operations on each node
    n_nodes (UInt32): number of nodes being used by the graph state
    stitching_properties (Uint32): data on the stitchability of the graph
"""
mutable struct AlgorithmSpecificGraph
    edge_data::Vector{AdjList}
    sqs::Vector{UInt8}
    sqp::Vector{UInt8}
    n_nodes::UInt32
    stitching_properties::StitchingProperties
end

function Base.show(io::IO, ag::AlgorithmSpecificGraph)
    # Convert edge_data to Int for decimal printing
    decimal_edge_data = [[Int(qubit) for qubit in adjList] for adjList in ag.edge_data]
    print(io, "AlgorithmSpecificGraph(\n  " *
              "edge_data = $decimal_edge_data,\n  " *
              "sqs = $(ag.sqs),\n  " *
              "sqp = $(ag.sqp),\n  " *
              "n_nodes = $(ag.n_nodes),\n  " *
              "stitching_properties = "
    )
    show(io, ag.stitching_properties)  # Use custom show method for readability
    println(io, "\n)")
end

# Create a graph with all qubits initialized to the |0> state.
AlgorithmSpecificGraphAllZero(max_graph_size, n_qubits) = AlgorithmSpecificGraph(
    [AdjList() for _ = 1:max_graph_size],
    fill(H_code, max_graph_size),
    fill(I_code, max_graph_size),
    n_qubits,
    StitchingProperties(false, false, n_qubits),
)

"""
Destructively convert edge_data to python adjacency list format.
"""
function python_adjlist!(adj)
    pylist([pylist(adj[i] .- 1) for i = eachindex(adj)])
end

function python_asg(asg)
    python_asg = Dict(
        "edge_data" => python_adjlist!(asg.edge_data),
        "sqs" => pylist(asg.sqs),
        "sqp" => pylist(asg.sqp),
        "data_nodes" => pylist(asg.stitching_properties.gate_output_nodes .- 1),
        "n_nodes" => asg.n_nodes,
        "stitching_properties" => python_stitching_properties(asg.stitching_properties),
    )
    return python_asg
end