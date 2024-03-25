################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
"""
Holds data for tracking conditional Pauli operators through a circuit.

    cond_paulis: Vector{Vector{Vector{Qubit}}}
        A vector containing the information on the conditional paulis
        for each qubit. The first index is the qubit which the pauli is
        conditioned on, the second index is the type of pauli (1 for X,
        2 for Z), and the third index is the qubit which the pauli
        acts on. For example, cond_paulis[3][1] = [6, 7] means that we must
        apply an X gate to qubits 6 and 7 if qubit 3 is measured to be 1.
    measurements: Vector{Vector{Union{UInt8,Float64}}}
        A vector containing the information on the measurements
        performed on each qubit. The first index is the qubit, and the
        vector contained in that index is the operation applied before
        measurement, the second index is the phase of the RZ gate. If
        the second index is 0.0, then no RZ gate is applied and the first
        index should not be RZ. We asume that an H gate is applied to
        each qubit before measurement right after the gate specified by
        the first index. For example, measurements[3] = [H_code, 0.0]
        means that we must apply an H gate to qubit 3 before measurement and
        measurements[3] = [RZ_code, 0.5] means that we must apply an RZ(0.5)
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