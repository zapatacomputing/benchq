using Jabalizer
using JSON

### ICM PART STARTS HERE

icm_compile(circuit, n_qubits) = Jabalizer.compile(circuit, n_qubits, ["T", "RX", "RY", "RZ"])

### JABALIZER PART STARTS HERE

const debug_flag = Ref(true)

function out_cnt(opcnt, prevcnt, tn, pt, t0)
    print("  Ops: $opcnt ($(opcnt-prevcnt)), ")
    print("elapsed: $(round((tn-t0)/60_000_000_000, digits=2)) min (")
    println(round((tn - pt) / 1_000_000_000, digits=2), " s)")
end

function icm_output_circuit(filename, circuit, data_qubits_map)
    dict = Dict()
    dict["circuit"] = circuit
    dict["data_qubits_map"] = data_qubits_map
    json_string = JSON.json(dict)

    open(filename, "w") do f
        write(f, json_string)
    end
end

function map_qubits(num_qubits, icm_output)
    qubit_map = Dict{String,Int}()
    for qubit in 1:num_qubits
        qubit_map[string(qubit - 1)] = qubit
    end
    for (op_name, op_qubits) in icm_output
        for qindex in op_qubits
            if !haskey(qubit_map, qindex)
                qubit_map[qindex] = (num_qubits += 1)
            end
        end
    end
    num_qubits, qubit_map
end

function prepare(num_qubits, qubit_map, icm_output)
    state = zero_state(num_qubits)
    chkcnt = prevbits = prevop = opcnt = 0
    pt = t0 = time_ns()
    # loops over all operations in the circuit and applies them to the state
    for (op_name, op_qubits) in icm_output
        opcnt += 1
        len = length(op_qubits)
        if len == 1
            (Jabalizer.gate_map[op_name](qubit_map[op_qubits[1]]))(state)
        elseif len == 2
            (Jabalizer.gate_map[op_name](qubit_map[op_qubits[1]], qubit_map[op_qubits[2]]))(state)
        else
            error("Too many arguments to $op_name: $len")
        end
        if debug_flag[] && (chkcnt += 1) > 99
            chkcnt = 0
            if ((tn = time_ns()) - pt >= 60_000_000_000)
                out_cnt(opcnt, prevop, tn, pt, t0)
                pt, prevop = tn, opcnt
            end
        end
    end
    debug_flag[] && out_cnt(opcnt, prevop, time_ns(), pt, t0)

    state
end

function run_jabalizer(circuit)
    # Convert to Julia values, and (as a temp hack) rename T_Dagger to T (until implemented)
    n_qubits = Jabalizer.pyconvert(Int, circuit.n_qubits)
    icm_input = Jabalizer.ICMGate[]
    for op in circuit.operations
        name = Jabalizer.pyconvert(String, op.gate.name)
        # TODO: THIS IS NOT CORRECT! TEMPORARY HACK!
        name == "T_Dagger" && (name = "T")
        indices = [string(Jabalizer.pyconvert(Int, qubit)) for qubit in op.qubit_indices]
        push!(icm_input, (name, indices))
    end

    print("ICM compilation: qubits=$n_qubits, gates=$(length(icm_input))\n\t")
    @time (icm_output, data_qubits_map) = icm_compile(icm_input, n_qubits)

    print("Output ICM circuit\n\t")
    @time icm_output_circuit("icm_output.json", icm_output, data_qubits_map)

    (n_qubits, qubit_map) = map_qubits(n_qubits, icm_output)

    print("Jabalizer state preparation: qubits=$n_qubits, gates=$(length(icm_output))\n\t")
    @time state = prepare(n_qubits, qubit_map, icm_output)

    print("Jabalizer graph generation: $n_qubits\n\t")
    @time (svec, op_seq) = graph_as_stabilizer_vector(state)

    print("Write Adjacency List: ")
    @time write_adjlist(svec, "adjacency_list.nxl")

    println("Jabalizer finished")
end
