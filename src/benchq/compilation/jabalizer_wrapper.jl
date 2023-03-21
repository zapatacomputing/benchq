using Jabalizer
using JSON

### ICM PART STARTS HERE


function icm_input(filename)
    raw_circuit = JSON.parsefile(filename)

    n_qubits = pop!(raw_circuit)
    circuit = Vector{Tuple{String,Vector{String}}}()

    for gate in raw_circuit
        gate_to_add = (gate[1], Vector{String}(gate[2]))
        append!(circuit, [gate_to_add])
    end
    n_qubits, circuit
end

icm_compile(circuit, n_qubits) = Jabalizer.compile(circuit, n_qubits, ["T", "RX", "RY", "RZ"])

function icm_output_circuit(filename, circuit, data_qubits_map)
    dict = Dict()
    dict["circuit"] = circuit
    dict["data_qubits_map"] = data_qubits_map
    json_string = JSON.json(dict)

    open(filename, "w") do f
        write(f, json_string)
    end
end

### JABALIZER PART STARTS HERE

const debug_flag = Ref(true)

function out_cnt(opcnt, prevcnt, tn, pt, t0)
    print("  Ops: $opcnt ($(opcnt-prevcnt)), ")
    print("elapsed: $(round((tn-t0)/60_000_000_000, digits=2)) min (")
    println(round((tn - pt) / 1_000_000_000, digits=2), " s)")
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

# This code is based on execute_cirq_circuit from Jabalizer

function prepare(num_qubits, qubit_map, icm_output)
    gate_map = Dict("I" => Jabalizer.Id,
        "H" => Jabalizer.H,
        "X" => Jabalizer.X,
        "Y" => Jabalizer.Y,
        "Z" => Jabalizer.Z,
        "CNOT" => Jabalizer.CNOT,
        "SWAP" => Jabalizer.SWAP,
        "S" => Jabalizer.P,
        "CZ" => Jabalizer.CZ)

    print("zero_state: ")
    @time state = zero_state(num_qubits)

    chkcnt = prevbits = prevop = opcnt = 0
    pt = t0 = time_ns()
    # loops over all operations in the circuit and applies them to the state
    for (op_name, op_qubits) in icm_output
        opcnt += 1
        len = length(op_qubits)
        if len == 1
            (gate_map[op_name](qubit_map[op_qubits[1]]))(state)
        elseif len == 2
            (gate_map[op_name](qubit_map[op_qubits[1]], qubit_map[op_qubits[2]]))(state)
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

print("Input ICM circuit\n\t")
@time (n_qubits, circuit) = icm_input("icm_input_circuit.json")

print("ICM compilation: qubits=$n_qubits, gates=$(length(circuit))\n\t")
@time (icm_output, data_qubits_map) = icm_compile(circuit, n_qubits)

print("Output ICM circuit\n\t")
@time icm_output_circuit("icm_output.json", icm_output, data_qubits_map)

print("Get total number of qubits\n\t")
@time (n_qubits, qubit_map) = map_qubits(n_qubits, icm_output)

print("Jabalizer state preparation: qubits=$n_qubits, gates=$(length(icm_output))\n\t")
@time state = prepare(n_qubits, qubit_map, icm_output)

print("Jabalizer graph generation: $n_qubits\n\t")
@time (svec, op_seq) = graph_as_stabilizer_vector(state)

print("Write Adjacency List: ")
@time write_adjlist(svec, "adjacency_list.nxl")

println("Jabalizer finished")
