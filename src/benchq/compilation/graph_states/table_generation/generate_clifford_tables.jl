# numbers which correspond to each of the gates in multiply_sqs
const I_code = UInt8(1)
const S_code = UInt8(2)
const H_code = UInt8(3)
const SQRT_X_code = UInt8(4)
const HSH_code = UInt8(4) # e^{iπ/4} X HSH = SHS
const SH_code = UInt8(5) # Apply H first, then S
const HS_code = UInt8(6) # Apply S first, then H

# Singe qubit Paulis
# external codes which must be distinct from the symplectic codes
const X_code = UInt8(7)
const Y_code = UInt8(8)
const Z_code = UInt8(9)

# Internal codes for the paulis. Allows for faster manipulation and simplifies debugging
const I_code_internal = UInt8(1)
const X_code_internal = UInt8(2)
const Y_code_internal = UInt8(3)
const Z_code_internal = UInt8(4)

const external_to_internal_paulis = Dict(
    I_code => I_code, X_code => X_code_internal, Y_code => Y_code_internal, Z_code => Z_code_internal
)

const multiply_sqp = [
    1 2 3 4
    2 1 4 3
    3 4 1 2
    4 3 2 1
]

update_pauli_from_S_from_left = zeros(Int, 4, 6)
const conj_pauli_by_S = [1, 3, 2, 4]
excess_pauli_S_left = [I_code, Z_code_internal, I_code, X_code_internal, Z_code_internal, X_code_internal]
for i in range(1, 4)
    for j in range(1, 6)
        update_pauli_from_S_from_left[i, j] = multiply_sqp[conj_pauli_by_S[i], excess_pauli_S_left[j]]
    end
end
println(update_pauli_from_S_from_left)

update_pauli_from_S_from_right = zeros(Int, 4, 6)
excess_pauli_S_right = [Z_code_internal, I_code, X_code_internal, X_code_internal, Z_code_internal, I_code]
for i in range(1, 4)
    for j in range(1, 6)
        excess_pauli = excess_pauli_S_right[j]
        update_pauli_from_S_from_right[i, j] = multiply_sqp[i, excess_pauli]
    end
end
println(update_pauli_from_S_from_right)


update_pauli_from_SQRT_X_from_right = zeros(Int, 4, 6)
excess_pauli_SQRT_X_right = [I_code, X_code_internal, I_code, X_code_internal, Z_code_internal, Z_code_internal]
for i in range(1, 4)
    for j in range(1, 6)
        excess_pauli = excess_pauli_SQRT_X_right[j]
        update_pauli_from_SQRT_X_from_right[i, j] = multiply_sqp[i, excess_pauli]
    end
end
println(update_pauli_from_SQRT_X_from_right)
