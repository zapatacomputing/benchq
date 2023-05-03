################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
#=
This contains the data required to run the graph simulation algorithm.
These tables are used to speed up the graph simulation algorithm by memoizing
the results of certain small calculations which are performed repeatedly.
=#

#=
"""
Lookup table for the decomposition of a local Clifford operation into a product of sqrt(X)
and sqrt(Z) gates. The index of the table corresponds to the local clifford operation.
The value of the table is a string of the form "UUVV" where U and V correspond to sqrt(X)
and sqrt(Z) gates respectively.
"""
const decomposition_lookup_table = [
    "UUUU",
    "UU",
    "VVUU",
    "VV",
    "VUU",
    "V",
    "VVV",
    "UUV",
    "UVU",
    "UVUUU",
    "UVVVU",
    "UUUVU",
    "UVV",
    "VVU",
    "UUU",
    "U",
    "VVVU",
    "UUVU",
    "VU",
    "VUUU",
    "UUUV",
    "UVVV",
    "UV",
    "UVUU",
]

function gen_decomp_tab(detab)
   out = UInt8[]
   for e in detab
      byt = 0x0
      for v in e
         byt = (byt << 1) | (v == 'V')
      end
      push!(out, byt | UInt8(length(e)<<5))
   end
   out
end
=#
"""
Lookup table for the decomposition of a local Clifford operation into a product of sqrt(X)
and sqrt(Z) gates. The index of the table corresponds to the local clifford operation.
The number of operations is stored in the upper 3 bits, and the lower 5 bits indicates
whether a sqrt(X) (0) or sqrt(Z) (1) gate is applied.
"""
const decomp_tab = [
    0x80, 0x40, 0x8c, 0x43, 0x64, 0x21, 0x67, 0x61, 0x62, 0xa8, 0xae, 0xa2,
    0x63, 0x66, 0x60, 0x20, 0x8e, 0x82, 0x42, 0x88, 0x81, 0x87, 0x41, 0x84
]

const LCO = UInt8 # code for local Clifford operation

"""
Lookup table for the product of two local clifford operations.
The index of the table corresponds to the first local clifford operation and the
value of the table corresponds to the second local clifford operation. The value
of the table is the local clifford operation that is the product of the two
local clifford operations.
"""
const multiply_lco = LCO[
     1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24
     2  1  4  3  7  8  5  6 12 11 10  9 14 13 16 15 20 19 18 17 23 24 21 22
     3  4  1  2  6  5  8  7 11 12  9 10 16 15 14 13 18 17 20 19 24 23 22 21
     4  3  2  1  8  7  6  5 10  9 12 11 15 16 13 14 19 20 17 18 22 21 24 23
     5  6  7  8  1  2  3  4 21 22 23 24 17 18 19 20 13 14 15 16  9 10 11 12
     6  5  8  7  3  4  1  2 24 23 22 21 18 17 20 19 16 15 14 13 11 12  9 10
     7  8  5  6  2  1  4  3 23 24 21 22 20 19 18 17 14 13 16 15 12 11 10  9
     8  7  6  5  4  3  2  1 22 21 24 23 19 20 17 18 15 16 13 14 10  9 12 11
     9 10 11 12 17 18 19 20  1  2  3  4 21 22 23 24  5  6  7  8 13 14 15 16
    10  9 12 11 19 20 17 18  4  3  2  1 22 21 24 23  8  7  6  5 15 16 13 14
    11 12  9 10 18 17 20 19  3  4  1  2 24 23 22 21  6  5  8  7 16 15 14 13
    12 11 10  9 20 19 18 17  2  1  4  3 23 24 21 22  7  8  5  6 14 13 16 15
    13 14 15 16 21 22 23 24 17 18 19 20  1  2  3  4  9 10 11 12  5  6  7  8
    14 13 16 15 23 24 21 22 20 19 18 17  2  1  4  3 12 11 10  9  7  8  5  6
    15 16 13 14 22 21 24 23 19 20 17 18  4  3  2  1 10  9 12 11  8  7  6  5
    16 15 14 13 24 23 22 21 18 17 20 19  3  4  1  2 11 12  9 10  6  5  8  7
    17 18 19 20  9 10 11 12 13 14 15 16  5  6  7  8 21 22 23 24  1  2  3  4
    18 17 20 19 11 12  9 10 16 15 14 13  6  5  8  7 24 23 22 21  3  4  1  2
    19 20 17 18 10  9 12 11 15 16 13 14  8  7  6  5 22 21 24 23  4  3  2  1
    20 19 18 17 12 11 10  9 14 13 16 15  7  8  5  6 23 24 21 22  2  1  4  3
    21 22 23 24 13 14 15 16  5  6  7  8  9 10 11 12  1  2  3  4 17 18 19 20
    22 21 24 23 15 16 13 14  8  7  6  5 10  9 12 11  4  3  2  1 19 20 17 18
    23 24 21 22 14 13 16 15  7  8  5  6 12 11 10  9  2  1  4  3 20 19 18 17
    24 23 22 21 16 15 14 13  6  5  8  7 11 12  9 10  3  4  1  2 18 17 20 19
]

# numbers which correspond to each of the gates in multiply_lco
const H_code        = LCO(11)
const S_code        = LCO(7)
const S_Dagger_code = LCO(6)
const SQRT_X_code   = LCO(15)
const CZ_code       = LCO(25)
const CNOT_code     = LCO(26)

const multiply_h = multiply_lco[H_code, :]
const multiply_s = multiply_lco[S_code, :]
const multiply_d = multiply_lco[S_Dagger_code, :]

const multiply_by_s = multiply_lco[:, S_code]
const multiply_by_sqrt_x = multiply_lco[:, SQRT_X_code]

# Packing functions to more efficiently store CZ data
c0(a,b) = UInt16((a<<8) | b)
c1(a,b) = c0(a,b) | 0x8000

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
    c1(1,1) c1(1,1) c1(1,4) c1(1,4) c1(1,6) c1(1,6) c1(1,7) c1(1,7) c0(4,9) c0(4,9) c0(1,11) c0(1,11) c1(1,4) c1(1,4) c1(1,1) c1(1,1) c1(1,7) c1(1,7) c1(1,6) c1(1,6) c0(1,11) c0(1,11) c0(4,9) c0(4,9)
    c1(1,1) c1(1,1) c1(1,4) c1(1,4) c1(1,6) c1(1,6) c1(1,7) c1(1,7) c0(3,9) c0(3,9) c0(1,11) c0(1,11) c1(1,4) c1(1,4) c1(1,1) c1(1,1) c1(1,7) c1(1,7) c1(1,6) c1(1,6) c0(1,11) c0(1,11) c0(3,9) c0(3,9)
    c1(3,4) c1(1,2) c1(1,3) c1(3,1) c1(1,5) c1(3,7) c1(3,6) c1(1,8) c0(1,9) c0(1,9) c0(3,11) c0(3,11) c1(1,3) c1(1,3) c1(1,2) c1(1,2) c1(1,8) c1(1,8) c1(1,5) c1(1,5) c0(3,11) c0(3,11) c0(1,9) c0(1,9)
    c1(4,1) c1(1,2) c1(1,3) c1(4,4) c1(1,5) c1(4,6) c1(4,7) c1(1,8) c0(1,9) c0(1,9) c0(4,11) c0(4,11) c1(1,3) c1(1,3) c1(1,2) c1(1,2) c1(1,8) c1(1,8) c1(1,5) c1(1,5) c0(4,11) c0(4,11) c0(1,9) c0(1,9)
    c1(5,4) c1(5,4) c1(5,1) c1(5,1) c1(5,7) c1(5,7) c1(5,6) c1(5,6) c0(7,9) c0(7,9) c0(5,11) c0(5,11) c1(5,1) c1(5,1) c1(5,4) c1(5,4) c1(5,6) c1(5,6) c1(5,7) c1(5,7) c0(5,11) c0(5,11) c0(7,9) c0(7,9)
    c1(6,1) c1(6,1) c1(6,4) c1(6,4) c1(6,6) c1(6,6) c1(6,7) c1(6,7) c0(7,9) c0(7,9) c0(6,11) c0(6,11) c1(6,4) c1(6,4) c1(6,1) c1(6,1) c1(6,7) c1(6,7) c1(6,6) c1(6,6) c0(6,11) c0(6,11) c0(7,9) c0(7,9)
    c1(7,1) c1(6,2) c1(6,3) c1(7,4) c1(6,5) c1(7,6) c1(7,7) c1(6,8) c0(6,9) c0(6,9) c0(7,11) c0(7,11) c1(6,3) c1(6,3) c1(6,2) c1(6,2) c1(6,8) c1(6,8) c1(6,5) c1(6,5) c0(7,11) c0(7,11) c0(6,9) c0(6,9)
    c1(7,1) c1(5,3) c1(5,2) c1(7,4) c1(5,8) c1(7,6) c1(7,7) c1(5,5) c0(5,9) c0(5,9) c0(7,11) c0(7,11) c1(5,2) c1(5,2) c1(5,3) c1(5,3) c1(5,5) c1(5,5) c1(5,8) c1(5,8) c0(7,11) c0(7,11) c0(5,9) c0(5,9)
    c0(9,4) c0(9,3) c0(9,1) c0(9,1) c0(9,7) c0(9,7) c0(9,6) c0(9,5) c0(9,9) c0(9,9) c0(9,11) c0(9,11) c0(9,1) c0(9,1) c0(9,3) c0(9,3) c0(9,5) c0(9,5) c0(9,7) c0(9,7) c0(9,11) c0(9,11) c0(9,9) c0(9,9)
    c0(9,4) c0(9,3) c0(9,1) c0(9,1) c0(9,7) c0(9,7) c0(9,6) c0(9,5) c0(9,9) c0(9,9) c0(9,11) c0(9,11) c0(9,1) c0(9,1) c0(9,3) c0(9,3) c0(9,5) c0(9,5) c0(9,7) c0(9,7) c0(9,11) c0(9,11) c0(9,9) c0(9,9)
    c0(11,1) c0(11,1) c0(11,3) c0(11,4) c0(11,5) c0(11,6) c0(11,7) c0(11,7) c0(11,9) c0(11,9) c0(11,11) c0(11,11) c0(11,3) c0(11,3) c0(11,1) c0(11,1) c0(11,7) c0(11,7) c0(11,5) c0(11,5) c0(11,11) c0(11,11) c0(11,9) c0(11,9)
    c0(11,1) c0(11,1) c0(11,3) c0(11,4) c0(11,5) c0(11,6) c0(11,7) c0(11,7) c0(11,9) c0(11,9) c0(11,11) c0(11,11) c0(11,3) c0(11,3) c0(11,1) c0(11,1) c0(11,7) c0(11,7) c0(11,5) c0(11,5) c0(11,11) c0(11,11) c0(11,9) c0(11,9)
    c1(3,4) c1(1,2) c1(1,3) c1(3,1) c1(1,5) c1(3,7) c1(3,6) c1(1,8) c0(1,9) c0(1,9) c0(3,11) c0(3,11) c1(1,3) c1(1,3) c1(1,2) c1(1,2) c1(1,8) c1(1,8) c1(1,5) c1(1,5) c0(3,11) c0(3,11) c0(1,9) c0(1,9)
    c1(3,4) c1(1,2) c1(1,3) c1(3,1) c1(1,5) c1(3,7) c1(3,6) c1(1,8) c0(1,9) c0(1,9) c0(3,11) c0(3,11) c1(1,3) c1(1,3) c1(1,2) c1(1,2) c1(1,8) c1(1,8) c1(1,5) c1(1,5) c0(3,11) c0(3,11) c0(1,9) c0(1,9)
    c1(1,1) c1(1,1) c1(1,4) c1(1,4) c1(1,6) c1(1,6) c1(1,7) c1(1,7) c0(3,9) c0(3,9) c0(1,11) c0(1,11) c1(1,4) c1(1,4) c1(1,1) c1(1,1) c1(1,7) c1(1,7) c1(1,6) c1(1,6) c0(1,11) c0(1,11) c0(3,9) c0(3,9)
    c1(1,1) c1(1,1) c1(1,4) c1(1,4) c1(1,6) c1(1,6) c1(1,7) c1(1,7) c0(3,9) c0(3,9) c0(1,11) c0(1,11) c1(1,4) c1(1,4) c1(1,1) c1(1,1) c1(1,7) c1(1,7) c1(1,6) c1(1,6) c0(1,11) c0(1,11) c0(3,9) c0(3,9)
    c1(7,1) c1(5,3) c1(5,2) c1(7,4) c1(5,8) c1(7,6) c1(7,7) c1(5,5) c0(5,9) c0(5,9) c0(7,11) c0(7,11) c1(5,2) c1(5,2) c1(5,3) c1(5,3) c1(5,5) c1(5,5) c1(5,8) c1(5,8) c0(7,11) c0(7,11) c0(5,9) c0(5,9)
    c1(7,1) c1(5,3) c1(5,2) c1(7,4) c1(5,8) c1(7,6) c1(7,7) c1(5,5) c0(5,9) c0(5,9) c0(7,11) c0(7,11) c1(5,2) c1(5,2) c1(5,3) c1(5,3) c1(5,5) c1(5,5) c1(5,8) c1(5,8) c0(7,11) c0(7,11) c0(5,9) c0(5,9)
    c1(5,4) c1(5,4) c1(5,1) c1(5,1) c1(5,7) c1(5,7) c1(5,6) c1(5,6) c0(7,9) c0(7,9) c0(5,11) c0(5,11) c1(5,1) c1(5,1) c1(5,4) c1(5,4) c1(5,6) c1(5,6) c1(5,7) c1(5,7) c0(5,11) c0(5,11) c0(7,9) c0(7,9)
    c1(5,4) c1(5,4) c1(5,1) c1(5,1) c1(5,7) c1(5,7) c1(5,6) c1(5,6) c0(7,9) c0(7,9) c0(5,11) c0(5,11) c1(5,1) c1(5,1) c1(5,4) c1(5,4) c1(5,6) c1(5,6) c1(5,7) c1(5,7) c0(5,11) c0(5,11) c0(7,9) c0(7,9)
    c0(11,1) c0(11,1) c0(11,3) c0(11,4) c0(11,5) c0(11,6) c0(11,7) c0(11,7) c0(11,9) c0(11,9) c0(11,11) c0(11,11) c0(11,3) c0(11,3) c0(11,1) c0(11,1) c0(11,7) c0(11,7) c0(11,5) c0(11,5) c0(11,11) c0(11,11) c0(11,9) c0(11,9)
    c0(11,1) c0(11,1) c0(11,3) c0(11,4) c0(11,5) c0(11,6) c0(11,7) c0(11,7) c0(11,9) c0(11,9) c0(11,11) c0(11,11) c0(11,3) c0(11,3) c0(11,1) c0(11,1) c0(11,7) c0(11,7) c0(11,5) c0(11,5) c0(11,11) c0(11,11) c0(11,9) c0(11,9)
    c0(9,4) c0(9,3) c0(9,1) c0(9,1) c0(9,7) c0(9,7) c0(9,6) c0(9,5) c0(9,9) c0(9,9) c0(9,11) c0(9,11) c0(9,1) c0(9,1) c0(9,3) c0(9,3) c0(9,5) c0(9,5) c0(9,7) c0(9,7) c0(9,11) c0(9,11) c0(9,9) c0(9,9)
    c0(9,4) c0(9,3) c0(9,1) c0(9,1) c0(9,7) c0(9,7) c0(9,6) c0(9,5) c0(9,9) c0(9,9) c0(9,11) c0(9,11) c0(9,1) c0(9,1) c0(9,3) c0(9,3) c0(9,5) c0(9,5) c0(9,7) c0(9,7) c0(9,11) c0(9,11) c0(9,9) c0(9,9)
]

const cz_connected = [
    c0(1,1) c0(4,1) c0(4,3) c0(1,4) c0(4,5) c0(1,6) c0(1,7) c0(4,7) c1(6,24) c1(6,23) c1(6,22) c1(6,21) c0(6,3) c0(7,3) c0(6,1) c0(7,1) c0(7,7) c0(6,7) c0(7,5) c0(6,5) c1(6,11) c1(6,12) c1(6,9) c1(6,10)
    c0(1,4) c0(3,3) c0(3,1) c0(1,1) c0(3,7) c0(1,7) c0(1,6) c0(3,5) c1(5,24) c1(5,23) c1(5,22) c1(5,21) c0(7,1) c0(5,1) c0(7,3) c0(5,3) c0(5,5) c0(7,5) c0(5,7) c0(7,7) c1(5,11) c1(5,12) c1(5,9) c1(5,10)
    c0(3,4) c0(1,3) c0(1,1) c0(3,1) c0(1,7) c0(3,7) c0(3,6) c0(1,5) c1(5,23) c1(5,24) c1(5,21) c1(5,22) c0(5,1) c0(7,1) c0(5,3) c0(7,3) c0(7,5) c0(5,5) c0(7,7) c0(5,7) c1(5,12) c1(5,11) c1(5,10) c1(5,9)
    c0(4,1) c0(1,1) c0(1,3) c0(4,4) c0(1,5) c0(4,6) c0(4,7) c0(1,7) c1(6,23) c1(6,24) c1(6,21) c1(6,22) c0(7,3) c0(6,3) c0(7,1) c0(6,1) c0(6,7) c0(7,7) c0(6,5) c0(7,5) c1(6,12) c1(6,11) c1(6,10) c1(6,9)
    c0(5,4) c0(7,3) c0(7,1) c0(5,1) c0(7,7) c0(5,7) c0(5,6) c0(7,5) c1(1,22) c1(1,21) c1(1,24) c1(1,23) c0(1,1) c0(3,1) c0(1,3) c0(3,3) c0(3,5) c0(1,5) c0(3,7) c0(1,7) c1(1,9) c1(1,10) c1(1,11) c1(1,12)
    c0(6,1) c0(7,1) c0(7,3) c0(6,4) c0(7,5) c0(6,6) c0(6,7) c0(7,7) c1(1,23) c1(1,24) c1(1,21) c1(1,22) c0(4,3) c0(1,3) c0(4,1) c0(1,1) c0(1,7) c0(4,7) c0(1,5) c0(4,5) c1(1,12) c1(1,11) c1(1,10) c1(1,9)
    c0(7,1) c0(6,1) c0(6,3) c0(7,4) c0(6,5) c0(7,6) c0(7,7) c0(6,7) c1(1,24) c1(1,23) c1(1,22) c1(1,21) c0(1,3) c0(4,3) c0(1,1) c0(4,1) c0(4,7) c0(1,7) c0(4,5) c0(1,5) c1(1,11) c1(1,12) c1(1,9) c1(1,10)
    c0(7,4) c0(5,3) c0(5,1) c0(7,1) c0(5,7) c0(7,7) c0(7,6) c0(5,5) c1(1,21) c1(1,22) c1(1,23) c1(1,24) c0(3,1) c0(1,1) c0(3,3) c0(1,3) c0(1,5) c0(3,5) c0(1,7) c0(3,7) c1(1,10) c1(1,9) c1(1,12) c1(1,11)
    c1(23,7) c1(21,6) c1(21,7) c1(23,6) c1(21,4) c1(23,1) c1(23,4) c1(21,1) c0(1,1) c0(1,3) c0(3,3) c0(3,1) c0(7,7) c0(5,5) c0(7,5) c0(5,7) c0(5,3) c0(7,1) c0(5,1) c0(7,3) c0(3,5) c0(3,7) c0(1,7) c0(1,5)
    c1(23,6) c1(21,7) c1(21,6) c1(23,7) c1(21,1) c1(23,4) c1(23,1) c1(21,4) c0(3,1) c0(3,3) c0(1,3) c0(1,1) c0(5,7) c0(7,5) c0(5,5) c0(7,7) c0(7,3) c0(5,1) c0(7,1) c0(5,3) c0(1,5) c0(1,7) c0(3,7) c0(3,5)
    c1(21,7) c1(21,8) c1(21,5) c1(21,6) c1(21,2) c1(21,1) c1(21,4) c1(21,3) c0(3,3) c0(3,1) c0(1,1) c0(1,3) c0(7,5) c0(5,7) c0(7,7) c0(5,5) c0(5,1) c0(7,3) c0(5,3) c0(7,1) c0(1,7) c0(1,5) c0(3,5) c0(3,7)
    c1(21,6) c1(21,5) c1(21,8) c1(21,7) c1(21,3) c1(21,4) c1(21,1) c1(21,2) c0(1,3) c0(1,1) c0(3,1) c0(3,3) c0(5,5) c0(7,7) c0(5,7) c0(7,5) c0(7,1) c0(5,3) c0(7,3) c0(5,1) c0(3,7) c0(3,5) c0(1,5) c0(1,7)
    c0(3,6) c0(1,7) c0(1,5) c0(3,7) c0(1,1) c0(3,4) c0(3,1) c0(1,3) c0(7,7) c0(7,5) c0(5,7) c0(5,5) c1(17,19) c1(17,20) c1(17,17) c1(17,18) c1(17,13) c1(17,14) c1(17,15) c1(17,16) c0(5,3) c0(5,1) c0(7,3) c0(7,1)
    c0(3,7) c0(1,5) c0(1,7) c0(3,6) c0(1,3) c0(3,1) c0(3,4) c0(1,1) c0(5,5) c0(5,7) c0(7,5) c0(7,7) c1(17,18) c1(17,17) c1(17,20) c1(17,19) c1(17,16) c1(17,15) c1(17,14) c1(17,13) c0(7,1) c0(7,3) c0(5,1) c0(5,3)
    c0(1,6) c0(3,7) c0(3,5) c0(1,7) c0(3,1) c0(1,4) c0(1,1) c0(3,3) c0(5,7) c0(5,5) c0(7,7) c0(7,5) c1(17,17) c1(17,18) c1(17,19) c1(17,20) c1(17,15) c1(17,16) c1(17,13) c1(17,14) c0(7,3) c0(7,1) c0(5,3) c0(5,1)
    c0(1,7) c0(3,5) c0(3,7) c0(1,6) c0(3,3) c0(1,1) c0(1,4) c0(3,1) c0(7,5) c0(7,7) c0(5,5) c0(5,7) c1(17,20) c1(17,19) c1(17,18) c1(17,17) c1(17,14) c1(17,13) c1(17,16) c1(17,15) c0(5,1) c0(5,3) c0(7,1) c0(7,3)
    c0(7,7) c0(5,5) c0(5,7) c0(7,6) c0(5,3) c0(7,1) c0(7,4) c0(5,1) c0(3,5) c0(3,7) c0(1,5) c0(1,7) c1(13,17) c1(13,18) c1(13,19) c1(13,20) c1(13,15) c1(13,16) c1(13,13) c1(13,14) c0(1,1) c0(1,3) c0(3,1) c0(3,3)
    c0(7,6) c0(5,7) c0(5,5) c0(7,7) c0(5,1) c0(7,4) c0(7,1) c0(5,3) c0(1,7) c0(1,5) c0(3,7) c0(3,5) c1(13,20) c1(13,19) c1(13,18) c1(13,17) c1(13,14) c1(13,13) c1(13,16) c1(13,15) c0(3,3) c0(3,1) c0(1,3) c0(1,1)
    c0(5,7) c0(7,5) c0(7,7) c0(5,6) c0(7,3) c0(5,1) c0(5,4) c0(7,1) c0(1,5) c0(1,7) c0(3,5) c0(3,7) c1(13,19) c1(13,20) c1(13,17) c1(13,18) c1(13,13) c1(13,14) c1(13,15) c1(13,16) c0(3,1) c0(3,3) c0(1,1) c0(1,3)
    c0(5,6) c0(7,7) c0(7,5) c0(5,7) c0(7,1) c0(5,4) c0(5,1) c0(7,3) c0(3,7) c0(3,5) c0(1,7) c0(1,5) c1(13,18) c1(13,17) c1(13,20) c1(13,19) c1(13,16) c1(13,15) c1(13,14) c1(13,13) c0(1,3) c0(1,1) c0(3,3) c0(3,1)
    c1(11,6) c1(9,7) c1(9,6) c1(11,7) c1(9,1) c1(11,4) c1(11,1) c1(9,4) c0(5,3) c0(5,1) c0(7,1) c0(7,3) c0(3,5) c0(1,7) c0(3,7) c0(1,5) c0(1,1) c0(3,3) c0(1,3) c0(3,1) c0(7,7) c0(7,5) c0(5,5) c0(5,7)
    c1(11,7) c1(9,6) c1(9,7) c1(11,6) c1(9,4) c1(11,1) c1(11,4) c1(9,1) c0(7,3) c0(7,1) c0(5,1) c0(5,3) c0(1,5) c0(3,7) c0(1,7) c0(3,5) c0(3,1) c0(1,3) c0(3,3) c0(1,1) c0(5,7) c0(5,5) c0(7,5) c0(7,7)
    c1(9,6) c1(9,5) c1(9,8) c1(9,7) c1(9,3) c1(9,4) c1(9,1) c1(9,2) c0(7,1) c0(7,3) c0(5,3) c0(5,1) c0(3,7) c0(1,5) c0(3,5) c0(1,7) c0(1,3) c0(3,1) c0(1,1) c0(3,3) c0(5,5) c0(5,7) c0(7,7) c0(7,5)
    c1(9,7) c1(9,8) c1(9,5) c1(9,6) c1(9,2) c1(9,1) c1(9,4) c1(9,3) c0(5,1) c0(5,3) c0(7,3) c0(7,1) c0(1,7) c0(3,5) c0(1,5) c0(3,7) c0(3,3) c0(1,1) c0(3,1) c0(1,3) c0(7,5) c0(7,7) c0(5,7) c0(5,5)
]
