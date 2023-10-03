# benchq

## What is it?

`benchq` estimates the required resources for performing a fault-tolerant computation using surface codes. It works with various inputs, such as circuits, openfermion QubitOperators, and pyscf files. Given correct input, `benchq` will return a list of resources required to perform the selected algorithm such as the required number of physical qubits, error rate, wall time, etc.

`benchq` was developed as a part of [DARPA Quantum Benchmarking program](https://www.darpa.mil/program/quantum-benchmarking).

## Installation

To install `benchq` run `pip install .` from the main directory.
It's been tested with Python 3.8-3.9 on macOS and Linux. Requires Jabalizer 0.4.3.

Known limitation: installation can fail because of a problem with `pyscf`, one of our transitive dependencies.
If you're a Windows user, please consider using [WSL](https://learn.microsoft.com/en-us/windows/wsl/install). On other systems you can try installing `pyscf` directly from its git repo: `pip install git+https://github.com/pyscf/pyscf@v2.0.1`.

### Extra dependencies

#### Julia
If you want to run the Graph State Compilation pipeline, you'll have to install Julia. Fortunately, benchq will install Julia automatically for you whenever it is needed if your current Julia installation is not compatible with the version of Julia that benchq requires. To avoid issues with conflicting versions, `juliapkg` do not install Julia in the typical {home}/.julia directory. We instead install julia within the python version you are using (if you are using a virtualenv, it will be installed in the file containing your virtualenv).

Note that running `julia` from the terminal may not give you access to the version of Julia that BenchQ installs. This is to prevent conflicts with other Julia installations you may have on your system. See the `juliapkg` documentation for more information.

#### PySCF
If you plan to use PySCF to generate Hamiltonians, use the `pyscf` install extra:
```bash
pip install '.[pyscf]'
```

#### Azure Quantum Resource Estimation
To run resource estimation using Azure Quantum Resource Estimation (QRE) tool, one needs to have Azure QRE package configured, please see [this tutorial](https://learn.microsoft.com/en-us/azure/quantum/intro-to-resource-estimation).

## Usage

Please take a look at the `examples` directory.
We have multiple examples there:
- `h_chain_trotter.py` shows how to use graph state compilation on a simple hydrogen chain example. (Requires `pyscf` install extra.)
- `resource_estimate_from_qasm.py` shows how to use graph state compilation when the circuit is loaded from QASM.
- `qsp_vlasov.py` shows how to perform resource estimation.

## Running benchmarks

To run the benchmarks run

``` bash
pytest benchmarks/
```

from the top-level directory of this repo. By default, this will skip some benchmarks that run extremely low. If you want to run
those too, set environmental variable `SLOW_BENCHMARKS` to any value, e.g.:

``` bash
SLOW_BENCHMARKS=1 pytest benchmarks/
```

Our benchmarks are run automatically on each release. You can see the performance of benchq over time on [benchq's benchmark page](https://zapatacomputing.github.io/benchq/dev/bench/).

## Development and Contribution

To install the development version, run `pip install -e '.[dev]'` from the main directory. (if using MacOS, you will need single quotes around the []. If using windows, or Linux, you might not need the quotes).

We use [Google-style](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) docstring format. If you'd like to specify types please use [PEP 484](https://www.python.org/dev/peps/pep-0484/) type hints instead adding them to docstrings.

There are codestyle-related [Github Actions](.github/workflows/style.yml) running for PRs. (TODO)

- If you'd like to report a bug/issue please create a new issue in this repository.
- If you'd like to contribute, please create a pull request to `main`.

### Running tests

Unit tests for this project can be run using `make coverage` command from the main directory.
Alternatively you can also run `pytest .`.

Since tests of integration with Azure QRE require additional setup, they are disabled by default. You can enable them by setting environmental variable `BENCHQ_TEST_AZURE` to any value.

### Style

We are using automatic tools for style and type checking. In order to make sure the code is compliant with them please run: `make style` from the main directory (this requires `dev` dependencies).
