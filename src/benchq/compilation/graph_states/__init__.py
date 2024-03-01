################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
import os
import pathlib

from .initialize_julia import jl, juliapkg
from .julia_utils import (
    get_algorithmic_graph_and_icm_output,
    get_algorithmic_graph_from_Jabalizer,
    compile_circuit_using_ruby_slippers,
    get_ruby_slippers_compiler,
)

jl.include(
    os.path.join(pathlib.Path(__file__).parent.resolve(), "jabalizer_wrapper.jl"),
)
jl.include(
    os.path.join(
        pathlib.Path(__file__).parent.resolve(), "ruby_slippers/ruby_slippers.jl"
    )
)
