import numpy as np

I = np.matrix([[1, 0], [0, 1]])  # noqa: E741

X = np.matrix([[0, 1], [1, 0]])
Y = np.matrix([[0, -1j], [1j, 0]])
Z = np.matrix([[1, 0], [0, -1]])

H = (2**-0.5) * np.matrix([[1, 1], [1, -1]])
S = np.matrix([[1, 0], [0, 1j]])  # type: ignore

CZ = np.matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, -1]])

ZERO_STATE = np.matrix([[1], [0], [0], [0]])
START_STATE = np.kron(H, H) * ZERO_STATE

SQS = {"I": I, "S": S, "H": H, "HSH": H * S * H, "SH": S * H, "HS": H * S}
SQP = {"I": I, "X": X, "Y": Y, "Z": Z}


def mat_conj(mat1, mat2):
    # conjuate matrix 1 by matrix 2
    return mat2 * mat1 * np.conj(mat2).T


score_symplectic = {"I": 400, "S": 400, "H": 100, "HSH": 200, "SH": 100, "HS": 200}
score_pauli = {"I": 5, "X": 1, "Y": 0, "Z": 1}

all_sqc = []
for S1_name, S1 in SQS.items():
    for P1_name, P1 in SQP.items():
        all_sqc += [(S1_name, S1, P1_name, P1)]

all_stab_group_perms = []
perms = [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
for connected_before_cz_was_applied in [False, True]:
    # order qubit 2 first to optimize for best operations on 2nd qubit
    for S1_name, S1, P1_name, P1 in all_sqc:
        for S2_name, S2, P2_name, P2 in all_sqc:
            clif = np.kron(P1 * S1, P2 * S2)
            if connected_before_cz_was_applied:
                clif = clif * CZ
            stab_1 = mat_conj(np.kron(X, I), clif)
            stab_2 = mat_conj(np.kron(I, X), clif)
            full_stab_group = [stab_1, stab_2, stab_1 * stab_2]
            for perm in perms:
                trial_stab_group_perm = np.array(
                    [np.round(full_stab_group[i - 1], 7) for i in perm]
                )
                all_stab_group_perms += [
                    (
                        connected_before_cz_was_applied,
                        S1_name,
                        P1_name,
                        S2_name,
                        P2_name,
                        trial_stab_group_perm,
                    )
                ]

cz_conj_pauli = {
    ("I", "I"): ("I", "I"),
    ("I", "X"): ("Z", "X"),
    ("I", "Y"): ("Z", "Y"),
    ("I", "Z"): ("I", "Z"),
    ("X", "I"): ("X", "Z"),
    ("X", "X"): ("Y", "Y"),
    ("X", "Y"): ("Y", "X"),
    ("X", "Z"): ("X", "I"),
    ("Y", "I"): ("Y", "Z"),
    ("Y", "X"): ("X", "Y"),
    ("Y", "Y"): ("X", "X"),
    ("Y", "Z"): ("Y", "I"),
    ("Z", "I"): ("Z", "I"),
    ("Z", "X"): ("I", "X"),
    ("Z", "Y"): ("I", "Y"),
    ("Z", "Z"): ("Z", "Z"),
}

pauli_mult_table = {
    ("I", "I"): "I",
    ("I", "X"): "X",
    ("I", "Y"): "Y",
    ("I", "Z"): "Z",
    ("X", "I"): "X",
    ("X", "X"): "I",
    ("X", "Y"): "Z",
    ("X", "Z"): "Y",
    ("Y", "I"): "Y",
    ("Y", "X"): "Z",
    ("Y", "Y"): "I",
    ("Y", "Z"): "X",
    ("Z", "I"): "Z",
    ("Z", "X"): "Y",
    ("Z", "Y"): "X",
    ("Z", "Z"): "I",
}

clif = np.kron(H, H) * CZ
stab_1 = mat_conj(np.kron(X, I), clif)
stab_2 = mat_conj(np.kron(I, X), clif)
full_stab_group = np.array([stab_1, stab_2, stab_1 * stab_2])  # type: ignore
for (
    trial_connected_before_cz_was_applied,
    trial_S1_name,
    trial_P1_name,
    trial_S2_name,
    trial_P2_name,
    trial_stab_group_perm,
) in all_stab_group_perms:
    if np.allclose(full_stab_group, trial_stab_group_perm, atol=1e-5):
        final_P1_name = pauli_mult_table["I", trial_P1_name]
        final_P2_name = pauli_mult_table["I", trial_P2_name]

        print(
            trial_connected_before_cz_was_applied,
            trial_S1_name,
            trial_P1_name,
            trial_S2_name,
            trial_P2_name,
        )
