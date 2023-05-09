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


def compute_lambda(h1, eri_full, sf_factors):
    """Compute lambda for Hamiltonian using SF method of Berry, et al.
    Args:
        pyscf_mf - PySCF mean field object
        sf_factors (ndarray) - (N x N x rank) array of SF factors from rank
            reduction of ERI
    Returns:
        lambda_tot (float) - lambda value for the single factorized Hamiltonian
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
