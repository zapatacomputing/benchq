#   Copyright 2017 The OpenFermion Developers
#   Modifications copyright 2023 Zapata Computing, Inc. to allow lambda to be calculated
#       from molecular integrals.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import numpy as np


def compute_lambda_sf(h1, eri_full, sf_factors):
    """Compute lambda for Hamiltonian using SF method of Berry, et al.

    Args:
        h1: Matrix elements of the one-body operator that includes kinetic
            energy operator and electorn-nuclear Coulomb operator.
        eri: Four-dimensional array containing electron-repulsion
            integrals.
        sf_factors: (N x N x rank) array of SF factors from rank
            reduction of ERI.

    Returns:
        lambda value for the single factorized Hamiltonian.
    """

    # Effective one electron operator contribution
    T = (
        h1
        - 0.5 * np.einsum("pqqs->ps", eri_full, optimize=True)
        + np.einsum("pqrr->pq", eri_full, optimize=True)
    )

    lambda_T = np.sum(np.abs(T))

    # Two electron operator contributions
    lambda_W = 0.25 * np.einsum(
        "ijP,klP->", np.abs(sf_factors), np.abs(sf_factors), optimize=True
    )
    lambda_tot = lambda_T + lambda_W

    return lambda_tot


def compute_lambda_df(h1, eri_full, df_factors):
    """Compute lambda for Hamiltonian using DF method of von Burg, et al.

    Args:
        h1: Matrix elements of the one-body operator that includes kinetic
            energy operator and electorn-nuclear Coulomb operator.
        eri: Four-dimensional array containing electron-repulsion
            integrals.
        df_factors: (N x N x rank) array of DF factors from ERI.

    Returns:
        lambda value for the double factorized Hamiltonian.
    """
    # one body contributions
    T = h1 - 0.5 * np.einsum("illj->ij", eri_full) + np.einsum("llij->ij", eri_full)
    e, _ = np.linalg.eigh(T)
    lambda_T = np.sum(np.abs(e))

    # two body contributions
    lambda_F = 0.0
    for vector in range(df_factors.shape[2]):
        Lij = df_factors[:, :, vector]
        # e, v = np.linalg.eigh(Lij)
        e = np.linalg.eigvalsh(Lij)  # just need eigenvals
        lambda_F += 0.25 * np.sum(np.abs(e)) ** 2

    lambda_tot = lambda_T + lambda_F

    return lambda_tot
