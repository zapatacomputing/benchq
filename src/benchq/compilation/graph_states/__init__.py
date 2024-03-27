################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
import os
import pathlib

from .circuit_compilers import (
    default_ruby_slippers_circuit_compiler,
    get_algorithmic_graph_and_icm_output,
    get_jabalizer_circuit_compiler,
    get_ruby_slippers_circuit_compiler,
)
from .implementation_compiler import get_implementation_compiler
from .initialize_julia import jl, juliapkg

jl.include(
    os.path.join(pathlib.Path(__file__).parent.resolve(), "jabalizer_wrapper.jl"),
)
jl.include(
    os.path.join(
        pathlib.Path(__file__).parent.resolve(), "ruby_slippers/ruby_slippers.jl"
    )
)
