# Bench-Q
Bench-Q provides tools for estimating the hardware resources required for fault-tolerant quantum computation. It includes a graph-state compiler, distillation factory models, decoder performance models, an ion-trap architecture model, implementations of selected quantum algorithms, and more.

Bench-Q was developed as a part of [DARPA Quantum Benchmarking program](https://www.darpa.mil/program/quantum-benchmarking).

## Installation

To install the latest released version of Bench-Q run `pip install benchq`.
It is tested with Python 3.9-3.11 on Linux and may or may not work with other Python versions or operating systems.

To use the development version of Bench-Q, clone this repository and run `pip install .` from the top-level directory.

### Extra dependencies

#### Julia
Although the Graph State Compilation pipeline requires Julia, you do not need to manually install it: benchq will install Julia automatically whenever it is needed if you do not already have a version of Julia that is compatible with Bench-Q installed.

Note that running `julia` from the terminal may not give you access to the version of Julia installed by Bench-Q. This is because JuliaPkg will install Julia in an isolated environment in order to avoid any potential conflicts with other versions of Julia that are already installed. See the [JuliaPkg documentation](https://github.com/JuliaPy/pyjuliapkg/blob/main/README.md) for more information about how Bench-Q installs Julia.

#### PySCF
If you plan to use PySCF to generate Hamiltonians, use the `pyscf` install extra:
```bash
pip install '.[pyscf]'
```

On some systems, the installation of PySCF can be problematic. If you're a Windows user, consider using [WSL](https://learn.microsoft.com/en-us/windows/wsl/install). You might also consider installing PySCF directly from its git repo: `pip install git+https://github.com/pyscf/pyscf@v2.2.1`.


#### Azure Quantum Resource Estimation
To run resource estimation using Azure Quantum Resource Estimation (QRE) tool, one needs to have Azure QRE package configure. See [this tutorial](https://learn.microsoft.com/en-us/azure/quantum/intro-to-resource-estimation) for more information.

#### Jabalizer
Jabalizer is an alternate graph state compilation toolchain to ruby slippers. To install Jabalizer, you will need to have the Rust programming language installed on your machine and run `pip install '.[jabalizer]'` from the top-level directory of this repository.

Jabalizer can provide drastically reduced resource counts for some circuits, but it is considerably slower than ruby slippers. It is recommended to use Jabalizer only for smaller circuits.

## Usage
See the [`examples`](examples) directory to learn more about how to use Bench-Q.

### Terminology Disambiguation

As fault-tolerant quantum computing is a relatively new field, there is no for several concepts which are crucial for resource estimation. We will try to clarify them here.

#### Problem Ingestion vs Problem Embedding vs Algorithm Implementation

`benchq` splits up the process of specifying a problem into three steps. The purpose of this is to split up the more complex parts of the process into more digestable, modular parts. The three steps are:

##### Problem ingestion

Take an input representing a problem instance and outputs data that needs to be loaded into the quantum computer. (e.g. the Hamiltonian we are simulating)

##### Problem embedding
Take the data from the problem ingestion step and embed it into a quantum circuit. (e.g. the block encoding circuit.) This can be a complicated process involving arithmetic and specialized compilation.

##### Algorithm implementation
Take the circuit from the problem embedding step and implement the algorithm. Also requires information from the problem instance to determine how to budget errors throughout the computation. (e.g. the required accuracy of the algorithm.)


## Running benchmarks

Because quantum compilation and resource estimation can be compute intensive, Bench-Q includes tools for benchmarking components that are potential bottlenecks. To run the benchmarks, execute the command

``` bash
pytest benchmarks/
```

from the top-level directory of this repo.

By default, this will skip some benchmarks that are extremely slow. If you want to run
those too, set environmental variable `SLOW_BENCHMARKS` to any value, e.g.:

``` bash
SLOW_BENCHMARKS=1 pytest benchmarks/
```

These benchmarks are run automatically on each release. You can see the performance of benchq over time on [benchq's benchmark page](https://zapatacomputing.github.io/benchq/dev/bench/).

## Development and Contribution

To install the development version, run `pip install -e '.[dev]'` from the main directory.

We use [Google-style](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) docstring format. If you'd like to specify types, please use [PEP 484](https://www.python.org/dev/peps/pep-0484/) type hints instead adding them to docstrings.
[Style checks](.github/workflows/style.yml) will automatically be run on pull requests.

- If you'd like to report a bug/issue please create a new issue in this repository.
- If you'd like to contribute, please create a pull request to `main`.

### Running tests

Unit tests for this project can be run using `make coverage` command from the main directory.
Alternatively you can also run `pytest .`.

Since tests of integration with Azure QRE require additional setup, they are disabled by default. You can enable them by setting environmental variable `BENCHQ_TEST_AZURE` to any value.

### Style

We are using automatic tools for style and type checking. In order to make sure the code is compliant with them please run: `make style` from the main directory (this requires `dev` dependencies).
