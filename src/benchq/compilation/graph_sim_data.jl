################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
#=
This contains the data required to run the graph simulation algorithm.
These tables are used to speed up the graph simulation algorithm by memoizing
the results of certain small calculations which are performed repeatedly.
=#

# numbers which correspond to each of the gates in multiply_UInt8
const Pauli_code = UInt8(1)
const S_code = UInt8(2)
const S_Dagger_code = UInt8(2) # S and S_Dagger are equal up to a pauli
const H_code = UInt8(3)
const SQRT_X_code = UInt8(4)
const SH_code = UInt8(5)
const HS_code = UInt8(6)

# Two qubit gates
const CZ_code = UInt8(7)
const CNOT_code = UInt8(8)

# Gates that get decomposed
const T_code = UInt8(9)
const T_Dagger_code = UInt8(10)
const RX_code = UInt8(11)
const RY_code = UInt8(12)
const RZ_code = UInt8(13)

const MEASURE_OFFSET = (RZ_code - T_code + 0x1)

# Measurement markers
const M_T_code = MEASURE_OFFSET + T_code
const M_T_Dagger_code = MEASURE_OFFSET + T_Dagger_code
const M_RX_code = MEASURE_OFFSET + RX_code
const M_RY_code = MEASURE_OFFSET + RY_code
const M_RZ_code = MEASURE_OFFSET + RZ_code

# enumerate the supported gates
const op_list = [
    "I",
    "X",
    "Y",
    "Z",
    "H",
    "S",
    "S_Dagger",
    "CZ",
    "CNOT",
    "T",
    "T_Dagger",
    "RX",
    "RY",
    "RZ",
    "SX",
    "SX_Dagger",
    "RESET",
]

# convert indices of supported gates to the corresponding code
const code_list = UInt8[
    0,
    0,
    0,
    0,
    H_code,
    S_code,
    S_Dagger_code,
    CZ_code,
    CNOT_code,
    T_code,
    T_Dagger_code,
    RX_code,
    RY_code,
    RZ_code,
    SQRT_X_code,
    SQRT_X_code,
    0,
]



#=
"""
Lookup table for the product of two local clifford operations.
The index of the table corresponds to the first local clifford operation and the
value of the table corresponds to the second local clifford operation. The value
of the table is the local clifford operation that is the product of the two
local clifford operations.
"""
const multiply_UInt8 = UInt8[
    1 2 3 4 5 6
    2 1 6 5 4 3
    3 5 1 6 2 4
    4 6 5 1 3 2
    5 3 4 2 6 1
    6 4 2 3 1 5
]

const _multiply_h = multiply_UInt8[H_code, :]
const _multiply_s = multiply_UInt8[S_code, :]
const _multiply_d = multiply_UInt8[S_Dagger_code, :]

const _multiply_by_s = multiply_UInt8[:, S_code]
const _multiply_by_sqrt_x = multiply_UInt8[:, SQRT_X_code]
=#

#=
Product of two local clifford operations:
   multiply_h & multiply_s store the results of multiplying h or s by the given value
   multiply_by_* store the results of multiplying the value by s (sqrt_z) or sqrt_x
   This is done by packing the row or column from the multiply_UInt8 table into a 32-bit
   unsigned integer, where each nibble is one of the values (all shifted up by 4 to avoid
   a shift at runtime.
=#
_unpack(c, v) = (c >> (v << 2)) & 0x7

multiply_h(v) = _unpack(0x4261530, v)
multiply_s(v) = _unpack(0x3456120, v)
multiply_by_s(v) = _unpack(0x4365120, v)
multiply_by_sqrt_x(v) = _unpack(0x3216540, v)

# Packing functions to more efficiently store CZ data
c0(a, b) = UInt8((a << 4) | b)
c1(a, b) = c0(a, b) | 0x80

"""
Lookup table for the product of a CZ gate and a local clifford operation.

The first and second indices of the table correspond to the local clifford operation on the
first and second nodes respectively.
The first value of the table is 0 if the the nodes are not connected
after applying the CZ gate and 1 if they are connected after applying the CZ gate.
The second and third values of the table are the local clifford operations on the
first and second nodes respectively after applying the CZ gate.
"""
const cz_isolated = [
    c1(1, 1) c1(1, 2) c0(1, 3) c1(1, 1) c1(1, 2) c0(1, 3)
    c1(2, 1) c1(2, 2) c0(2, 3) c1(2, 1) c1(2, 2) c0(2, 3)
    c0(3, 1) c0(3, 2) c0(3, 3) c0(3, 1) c0(3, 2) c0(3, 3)
    c1(1, 1) c1(1, 2) c0(1, 3) c1(1, 1) c1(1, 2) c0(1, 3)
    c1(2, 1) c1(2, 2) c0(2, 3) c1(2, 1) c1(2, 2) c0(2, 3)
    c0(3, 1) c0(3, 2) c0(3, 3) c0(3, 1) c0(3, 2) c0(3, 3)
]
const cz_connected = [
    c0(1, 1) c0(1, 2) c1(2, 6) c0(2, 1) c0(2, 2) c1(2, 3)
    c0(2, 1) c0(2, 2) c1(1, 6) c0(1, 1) c0(1, 2) c1(1, 3)
    c1(6, 2) c1(6, 1) c0(1, 1) c0(2, 2) c0(2, 1) c0(1, 2)
    c0(1, 2) c0(1, 1) c0(2, 2) c1(5, 5) c1(5, 4) c0(2, 1)
    c0(2, 2) c0(2, 1) c0(1, 2) c1(4, 5) c1(4, 4) c0(1, 1)
    c1(3, 2) c1(3, 1) c0(2, 1) c0(1, 2) c0(1, 1) c0(2, 2)
]
