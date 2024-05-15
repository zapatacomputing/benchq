################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
import os
import pathlib

from pkg_resources import WorkingSet

from .circuit_compilers import (
    default_ruby_slippers_circuit_compiler,
    get_algorithmic_graph_and_icm_output,
    get_jabalizer_circuit_compiler,
    get_ruby_slippers_circuit_compiler,
)
from .implementation_compiler import get_implementation_compiler
from .initialize_julia import jl, juliapkg

jabalizer_dependencies = ["pauli-tracker", "mbqc-scheduling"]
installed_packages = {pkg.key for pkg in WorkingSet()}
current_directory = pathlib.Path(__file__).parent.resolve()
if all(dep in installed_packages for dep in jabalizer_dependencies):
    jl.include(os.path.join(current_directory, "jabalizer_wrapper.jl"))
jl.include(os.path.join(current_directory, "ruby_slippers/ruby_slippers.jl"))
