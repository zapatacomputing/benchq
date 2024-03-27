using Jabalizer
using Graphs
using PythonCall
import Graphs.SimpleGraphs

function run_jabalizer(circuit, optimization, debug_flag=false, space_optimization_timeout=1)

    asg, pauli_tracker, best_path = get_jabalizer_graph_state_data(
        circuit, optimization, debug_flag, space_optimization_timeout
    )


    println("here!")
    println(asg)
    println(pauli_tracker)

    num_logical_qubits = get_num_logical_qubits(pauli_tracker.layering, asg, optimization, debug_flag)
    debug_flag && println("Running substrate scheduler...")
    if debug_flag && num_logical_qubits == parse(Int, "$(best_path.time)") && optimization == "Space"
        error("Jabalizer and Ruby Slippers disagree on qubit counts.")
    end
    num_layers = parse(Int, "$(best_path.time)")
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
        "graph_creation_tocks_per_layer" => graph_creation_tocks_per_layer,
        "t_states_per_layer" => t_states_per_layer,
        "rotations_per_layer" => rotations_per_layer,
    )

    return python_compiled_data
end


function get_jabalizer_graph_state_data(circuit, optimization, debug_flag=false, space_optimization_timeout=1)
    if debug_flag
        println("Compiling using Jabalizer...")
        println("Converting to Jabalizer Circuit...")
    end

    registers = [i for i in 1:pyconvert(Int, circuit.n_qubits)]
    println("circuit: $(circuit)")

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

    jabalizer_quantum_circuit = Jabalizer.QuantumCircuit(
        registers,
        input_circuit
    )

    if debug_flag
        println("Compiling to Algorithm Specific Graph...")
    end

    mbqc_scheduling = pyimport("mbqc_scheduling")
    SpacialGraph = pyimport("mbqc_scheduling").SpacialGraph
    PartialOrderGraph = pyimport("mbqc_scheduling").PartialOrderGraph

    graph, loc_corr, mseq, data_qubits, frames_array = Jabalizer.gcompile(
        jabalizer_quantum_circuit;
        universal=true,
        ptracking=true,
        teleport=["T", "T_Dagger", "RZ"]
    )
    graph_input_nodes = Vector{Qubit}(eval(Meta.parse("$(data_qubits.state)")))
    graph_output_nodes = Vector{Qubit}(eval(Meta.parse("$(data_qubits.output)")))

    measurements = []
    for gate in mseq
        if gate.name == "T"
            push!(measurements, [T_code, 0.0])
        elseif gate.name == "T_Dagger"
            push!(measurements, [T_Dagger_code, 0.0])
        elseif gate.name == "RZ"
            # Jabalizer doesn't keep track of the angles of rotations yet
            push!(measurements, [RZ_code, 0.0])
        elseif gate.name == "X"
            push!(measurements, [H_code, 0.0])
        else
            error("Invalid measurement type.")
        end
    end

    frames, frame_flags, buffer, buffer_flags = frames_array

    sparse_rep = SimpleGraphs.adj(graph)
    # prepare graph to be scheudled by mbqc_scheduling
    python_sparse_rep = [e .- 1 for e in sparse_rep]
    for (s, i) in zip(data_qubits[:state], data_qubits[:input])
        insert!(python_sparse_rep, s, [i])
        println("s: $(s), i: $(i)")
    end
    python_sparse_rep = SpacialGraph(python_sparse_rep)

    # make sparse rep compatible with benchq
    sparse_rep = eval(Meta.parse("$(sparse_rep)"))
    benchq_sparse_rep = Vector{Set{Qubit}}([])
    for neighborhood in sparse_rep
        push!(benchq_sparse_rep, Set([]))
        for neighbor in neighborhood
            push!(benchq_sparse_rep[end], Qubit(neighbor))
        end
    end


    for (o, i, s) in zip(data_qubits[:output], data_qubits[:input], data_qubits[:state])
        push!(benchq_sparse_rep, Set([i]))
        push!(benchq_sparse_rep[i], s)
    end

    order = frames.get_py_order(frame_flags)
    order = PartialOrderGraph(order)

    debug_flag && println("Ordering non-clifford measurements...")
    index_of_best_path = 1
    if optimization == "Time"
        # Find time optimal paths
        paths = mbqc_scheduling.run(python_sparse_rep, order)
        all_paths = paths.into_py_paths()
        # extract the most time efficient path
        num_layers = typemax(UInt)
        for (this_path_index, path) in enumerate(all_paths)
            converted_time = parse(Int, "$(path.space)")
            if converted_time < num_layers
                num_layers = converted_time
                index_of_best_path = this_path_index
            end
        end
    elseif optimization == "Space"
        # Search probabilistially for space optimal path
        AcceptFunc = pyimport("mbqc_scheduling.probabilistic").AcceptFunc
        paths = mbqc_scheduling.run(
            python_sparse_rep,
            order;
            do_search=true,
            nthreads=1,
            timeout=space_optimization_timeout,
            probabilistic=(AcceptFunc(), nothing)
        )
        all_paths = paths.into_py_paths()
        # extract the most space efficient path
        num_logical_qubits = typemax(Qubit)
        for (this_path_index, path) in enumerate(all_paths)
            converted_space = parse(Int, "$(path.space)")
            if converted_space < num_logical_qubits
                num_logical_qubits = converted_space
                index_of_best_path = this_path_index
            end
        end
    elseif optimization == "Variable"
        error("Variable optimization not implemented for jaablizer compiler.")
    end

    index_of_best_path -= 1

    # add dummy nodes in ASG that would represent the next nodes to teleport to
    # as these are not included in the current version of the jabalizer output.
    # This will result in a slight underestimate of resources that will be
    # corrected once Jabalizer is updated.
    layering = eval(Meta.parse("$(all_paths[index_of_best_path].steps)"))
    layering = Vector{Vector{Qubit}}([e .+ 1 for e in layering])
    for _ in 1:num_circuit_qubits
        push!(measurements, [H_code, 0.0])
    end
    # dummy asg and pauli tracker for substrate scheduler
    n_nodes = length(benchq_sparse_rep)
    asg = AlgorithmSpecificGraph(
        benchq_sparse_rep,
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

    return asg, pauli_tracker, all_paths[index_of_best_path]
end