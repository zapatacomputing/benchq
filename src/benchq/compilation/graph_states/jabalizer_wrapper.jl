using Jabalizer
using Graphs
using PythonCall
import Graphs.SimpleGraphs

function run_jabalizer(circuit, optimization, debug_flag=false, space_optimization_timeout=1)

    asg, pauli_tracker, num_layers = get_jabalizer_graph_state_data(
        circuit, optimization, debug_flag, space_optimization_timeout
    )

    num_logical_qubits = get_num_logical_qubits(pauli_tracker.layering, asg, optimization, debug_flag)
    debug_flag && println("Running substrate scheduler...")
    if debug_flag && num_logical_qubits == num_layers && optimization == "Space"
        error("Jabalizer and Ruby Slippers disagree on qubit counts.")
    end
    (graph_creation_tocks_per_layer, t_states_per_layer, rotations_per_layer) =
        two_row_scheduler(
            asg,
            pauli_tracker,
            num_logical_qubits,
            optimization,
            debug_flag,
        )

    python_compiled_data = Dict(
        "num_logical_qubits" => num_logical_qubits,
        "num_layers" => num_layers,
        "graph_creation_tocks_per_layer" => pylist(graph_creation_tocks_per_layer),
        "t_states_per_layer" => pylist(t_states_per_layer),
        "rotations_per_layer" => pylist(rotations_per_layer),
    )

    return python_compiled_data
end


function get_jabalizer_graph_state_data(circuit, optimization, debug_flag=false, space_optimization_timeout=1)
    if debug_flag
        println("Compiling using Jabalizer...")
        println("Converting to Jabalizer Circuit...")
    end

    # Reading and caching the orquestra circuit
    input_circuit::Vector{Jabalizer.Gate} = []
    num_circuit_qubits = pyconvert(Int, circuit.n_qubits)
    measurements = Vector{Vector{Union{UInt8,Float64}}}([[H_code, 0.0] for _ in range(1, num_circuit_qubits)])
    for op in circuit.operations
        # reset operation is not supported by jabalizer yet
        if occursin("ResetOperation", pyconvert(String, op.__str__())) # reset operation
            @warn "Circuit contains the 'reset' operation, which is not supported by Jabalizer. Skipping..."
            continue
        else
            if Jabalizer.pyconvert(String, op.gate.name) == "S_Dagger"
                new_gate = Jabalizer.Gate(
                    "S_DAG",
                    [],
                    [Jabalizer.pyconvert(Int, qubit) + 1 for qubit in op.qubit_indices]
                )
            elseif Jabalizer.pyconvert(String, op.gate.name) == "I"
                continue
            elseif Jabalizer.pyconvert(String, op.gate.name) == "RZ"
                new_gate = Jabalizer.Gate(
                    "RZ",
                    [Jabalizer.pyconvert(Float64, op.gate.params[0])],
                    [Jabalizer.pyconvert(Int, qubit) + 1 for qubit in op.qubit_indices]
                )
            else
                new_gate = Jabalizer.Gate(
                    Jabalizer.pyconvert(String, op.gate.name),
                    [],
                    [Jabalizer.pyconvert(Int, qubit) + 1 for qubit in op.qubit_indices]
                )
            end

        end
        push!(input_circuit, new_gate)
        for qubit in op.qubit_indices
            num_circuit_qubits = max(num_circuit_qubits, pyconvert(Int, qubit) + 1)
        end
    end

    registers = [i for i in 1:pyconvert(Int, circuit.n_qubits)]

    jabalizer_quantum_circuit = Jabalizer.QuantumCircuit(
        registers,
        input_circuit
    )

    if debug_flag
        println("Compiling to Algorithm Specific Graph...")
    end

    jabalizer_out = Jabalizer.mbqccompile(
        jabalizer_quantum_circuit;
        universal=true,
        ptracking=true,
        teleport=["T", "T_Dagger", "RZ"]
    )

    n_nodes = length(jabalizer_out["spatialgraph"])
    julia_spacial_graph = [Set{UInt32}(neighborhood .+ 1) for neighborhood in jabalizer_out["spatialgraph"]]
    graph_input_nodes = jabalizer_out["statenodes"] .+ 1
    graph_output_nodes = jabalizer_out["outputnodes"] .+ 1


    measurements = [[] for _ in 1:n_nodes]
    for gate in jabalizer_out["measurements"]
        if gate[1] == "T"
            measurements[gate[2]+1] = [T_code, 0.0]
        elseif gate[1] == "T_Dagger"
            measurements[gate[2]+1] = [T_Dagger_code, 0.0]
        elseif gate[1] == "RZ"
            # Jabalizer doesn't keep track of the angles of rotations yet
            measurements[gate[2]+1] = [T_Dagger_code, gate[3]]
        elseif gate[1] == "X"
            measurements[gate[2]+1] = [H_code, 0.0]
        else
            error("Invalid measurement type.")
        end
    end

    layering = [layer .+ 1 for layer in jabalizer_out["steps"]]

    asg = AlgorithmSpecificGraph(
        julia_spacial_graph,
        [],
        [],
        n_nodes,
        StitchingProperties(
            true,
            true,
            graph_input_nodes,
            graph_output_nodes,
            [],
        ),
    )
    pauli_tracker = PauliTracker(
        Vector{Vector{Vector{Qubit}}}([[[], []] for _ in 1:n_nodes]),
        measurements,
        n_nodes,
        layering,
        optimization,
        1,
        1,
        false,
    )

    return asg, pauli_tracker, length(jabalizer_out["steps"])
end