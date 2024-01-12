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

    StitchingProperties(takes_graph_input, gives_graph_output, n_qubits) = new(
        takes_graph_input,
        gives_graph_output,
        [],
        [],
        [Qubit(i) for i = 1:n_qubits]
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
Data on the aglortihm specific graph state. During computation, this
struct may contain more nodes than are actually used in the graph state.
At the end of the computation, the data structures are resized to only
contain the nodes which are actually used in the graph state. A lack
of input and output nodes indicate that this graph is not stitchable.

Attributes:
    edge_data (Vector{AdjList}): adjacency list describing the graph
    sqs (Vector{UInt8}): single qubit clifford operations on each node
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
# Create a graph with all qubits initialized to the |0> state.
AlgorithmSpecificGraphAllZero(max_graph_size, n_qubits) = AlgorithmSpecificGraph(
    [AdjList() for _ = 1:max_graph_size],
    fill(H_code, max_graph_size),
    fill(I_code, max_graph_size),
    n_qubits,
    StitchingProperties(false, false, n_qubits),
)


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