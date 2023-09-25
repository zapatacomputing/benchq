################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
import os
import pathlib

print("made it here!")
from juliacall import Main as jl

print("now here!")

from .julia_utils import (
    get_algorithmic_graph_and_icm_output,
    get_algorithmic_graph_from_Jabalizer,
    get_algorithmic_graph_from_ruby_slippers,
    get_ruby_slippers_compiler,
)
from .pyliqtr_transpilation import pyliqtr_transpile_to_clifford_t
from .transpile_to_native_gates import transpile_to_native_gates

import juliapkg

juliapkg.require_julia("1.9.3")
juliapkg.add("JSON", "682c06a0-de6a-54ab-a142-c8b1cf79cde6", version="0.21")
juliapkg.add("Jabalizer", "5ba14d91-d028-496b-b148-c0fbc366f709", version="0.4.4")
juliapkg.add("TimerOutputs", "a759f4b9-e2f1-59dc-863e-4aeb61b1ea8f", version="0.5.23")
juliapkg.add("StatsBase", "2913bbd2-ae8a-5f71-8c99-4fb6c76f3a91", version="0.34.0")

juliapkg.resolve()

jl.include(
    os.path.join(pathlib.Path(__file__).parent.resolve(), "jabalizer_wrapper.jl"),
)
jl.include(os.path.join(pathlib.Path(__file__).parent.resolve(), "ruby_slippers.jl"))
