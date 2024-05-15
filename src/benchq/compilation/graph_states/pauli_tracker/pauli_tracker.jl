################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
"""
Holds data for tracking conditional Pauli operators through a circuit.

    cond_paulis: Vector{Vector{Vector{Qubit}}}
        A vector containing the information on the conditional paulis
        for each qubit. The first index is the qubit which the pauli is
        conditioned on, the second index is the type of pauli (1 for X,
        2 for Z). The innermost vector is the list of target qubit indices.         
        For example, cond_paulis[3][1] = [6, 7] means that we must
        apply an X gate to qubits 6 and 7 if qubit 3 is measured to be 1.
    measurements: Vector{Vector{Union{UInt8,Float64}}}
        A vector containing the information on the basis in which each
        qubit is measured. We assume that two operations will be applied before
        measurement in the Z basis: the first is specified by this array and the second
        is always a Hadamard gate. The first index of the measurements array is the
        qubit index, and the vector contained in that index describes the operation to
        be applied before the Hadamard. The first element is the tye of operation, and
        if the operation is an RZ, then the second element is the phase of the RZ gate.
        If the operation is not an RZ, the second element is zero.
        For example, measurements[3] = [H_code, 0.0] means that we must apply two H
        gates (i.e. identity) to qubit 3 before measurement and
        measurements[3] = [RZ_code, 0.5] means that we must apply RZ(0.5) followed by H
        before measurement.
    n_nodes: Qubit
        The number of qubits in the circuit.
    layering: Vector{Vector{Qubit}}
        A vector containing order in which the qubits must be measured.
        The first index is the layer, and the vector contained in that
        index is the qubits in that layer. The qubits in each layer are
        measured in parallel.
    layering_optimization: String
        The optimization used to calculate the layering. Can be "Time",
        "Space", and "Variable".
    max_num_qubits: Int
        The width parameter used for the "Variable" optimization. Corresponds
        to the maximum number of qubits which can exist at each time step.
        Note that if one picks max_num_qubits to be too small, we will
        resort to the smallest width which can fit the circuit.
    optimal_dag_density: Int
        The optimal density of the DAG. This quantity roughly corresponds to
        how well defined the "arrow of time" is in the DAG. A higher number
        means that the DAG is less well defined and so the DAG might be more
        difficult to create, but is more optimizable. Ranges from 0-infinity.
        This variable is used in every dag optimizeation other than
"""
mutable struct PauliTracker
    cond_paulis::Vector{Vector{Vector{Qubit}}}
    measurements::Vector{Vector{Union{UInt8,Float64}}}
    n_nodes::Qubit
    layering::Vector{Vector{Qubit}}
    layering_optimization::String
    max_num_qubits::Int
    optimal_dag_density::Int
    use_fully_optimized_dag::Bool

    PauliTracker(cond_paulis, measurements, n_nodes, layering, layering_optimization, max_num_qubits, optimal_dag_density, use_fully_optimized_dag) = new(
        cond_paulis,
        measurements,
        n_nodes,
        layering,
        layering_optimization,
        max_num_qubits,
        optimal_dag_density,
        use_fully_optimized_dag,
    )

    PauliTracker(n_qubits, layering_optimization, max_num_qubits, optimal_dag_density, use_fully_optimized_dag) = new(
        [[[], []] for _ in range(1, n_qubits)],
        [[H_code, 0.0] for _ in range(1, n_qubits)],
        n_qubits,
        [],
        layering_optimization,
        max_num_qubits,
        optimal_dag_density,
        use_fully_optimized_dag,
    )
end

function Base.show(io::IO, pt::PauliTracker)
    # Helper function to convert nested Qubit vectors to decimal format
    function convert_to_decimal(v)
        if typeof(v) == Qubit
            return Int(v)  # Convert Qubit to Int for decimal printing
        elseif typeof(v) <: AbstractVector
            return [convert_to_decimal(e) for e in v]  # Recursively convert elements
        else
            return v  # Return non-vector elements unchanged
        end
    end

    print(io, "PauliTracker(\n")
    print(io, "  cond_paulis = $(convert_to_decimal(pt.cond_paulis)),\n")
    print(io, "  measurements = $(pt.measurements),\n")  # Assumes measurements are already in a printable format
    print(io, "  n_nodes = $(Int(pt.n_nodes)),\n")  # Convert n_nodes to Int for decimal printing
    print(io, "  layering = $(convert_to_decimal(pt.layering)),\n")
    print(io, "  layering_optimization = \"$(pt.layering_optimization)\",\n")
    print(io, "  max_num_qubits = $(pt.max_num_qubits),\n")
    print(io, "  optimal_dag_density = $(pt.optimal_dag_density),\n")
    print(io, "  use_fully_optimized_dag = $(pt.use_fully_optimized_dag)\n")
    print(io, ")")
end

"""Convert pauli tracker to a python object"""
function python_pauli_tracker(pauli_tracker)
    python_cond_paulis = []
    for node in pauli_tracker.cond_paulis
        push!(python_cond_paulis, pylist([pylist(node[1] .- 1), pylist(node[2] .- 1)]))
    end

    python_pauli_tracker = Dict(
        "cond_paulis" => pylist(python_cond_paulis),
        "measurements" => pylist(pauli_tracker.measurements),
        "n_nodes" => pauli_tracker.n_nodes,
        "layering" => python_adjlist!(pauli_tracker.layering),
        "layering_optimization" => pauli_tracker.layering_optimization,
        "max_num_qubits" => pauli_tracker.max_num_qubits,
        "optimal_dag_density" => pauli_tracker.optimal_dag_density,
        "use_fully_optimized_dag" => pauli_tracker.use_fully_optimized_dag,
    )

    return python_pauli_tracker
end

function add_new_qubit_to_pauli_tracker!(pauli_tracker::PauliTracker)
    push!(pauli_tracker.cond_paulis, [[], []])
    push!(pauli_tracker.measurements, [H_code, 0.0])
    pauli_tracker.n_nodes += 1
end

"""
Add a conditional Pauli operator to the PauliTracker object.
"""

function add_z_to_pauli_tracker!(
    cond_paulis::Vector{Vector{Vector{Qubit}}},
    control_qubit::Qubit,
    target_qubit::Qubit,
)
    push!(cond_paulis[target_qubit][2], control_qubit)
end

function add_x_to_pauli_tracker!(
    cond_paulis::Vector{Vector{Vector{Qubit}}},
    control_qubit::Qubit,
    target_qubit::Qubit,
)
    push!(cond_paulis[target_qubit][1], control_qubit)
end

"""
Indicate that a node is being measured.
"""

function add_measurement!(measurements, op_code::UInt8, qubit::Qubit)
    measurements[qubit][1] = op_code
end

function add_measurement!(measurements, op_code::UInt8, qubit::Qubit, phase::Float64)
    measurements[qubit][1] = op_code
    measurements[qubit][2] = phase
end

"""
Functions for tracking the paulis through gates.
"""

function track_conditional_paulis_through_h(
    cond_paulis::Vector{Vector{Vector{Qubit}}},
    qubit,
)
    x_cond_paulis = cond_paulis[qubit][1]
    cond_paulis[qubit][1] = cond_paulis[qubit][2]
    cond_paulis[qubit][2] = x_cond_paulis
end

function track_conditional_paulis_through_s(
    cond_paulis::Vector{Vector{Vector{Qubit}}},
    qubit,
)
    for x_control in cond_paulis[qubit][1]
        toggle_pauli_z(cond_paulis, x_control, qubit)
    end


end

function track_conditional_paulis_through_cz(
    cond_paulis::Vector{Vector{Vector{Qubit}}},
    qubit_1,
    qubit_2,
)
    for x_control in cond_paulis[qubit_1][1]
        toggle_pauli_z(cond_paulis, x_control, qubit_2)
    end
    for x_control in cond_paulis[qubit_2][1]
        toggle_pauli_z(cond_paulis, x_control, qubit_1)
    end
end

"""
If a controlled Z exists on the target qubit, then we get rid of it.
If a controlled Z doesn't exist on the target qubit, then we add one.
"""
function toggle_pauli_z(cond_paulis, toggled_qubit, target_qubit)
    if toggled_qubit in cond_paulis[target_qubit][2]
        setdiff!(cond_paulis[target_qubit][2], [toggled_qubit])
    else
        push!(cond_paulis[target_qubit][2], toggled_qubit)
    end
end


include("dag_creation.jl")
include("dag_layering.jl")
include("dag_layering_properties.jl")