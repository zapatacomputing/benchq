# The Ruby Slippers Compiler

Here we provide tools for compiling a quantum program written in Julia. This is probably the most complex section of benchq where we keep most of the unique tools that BenchQ provides. The main tool we provide is the Ruby Slippers compiler, which is a Julia compiler that can be called from Python. This compiler is designed to be used with the [Orquestra](https://www.zapatacomputing.com/orquestra/) quantum computing platform, but translating from other platforms to orquestra should be relatively straightforward.

This code works particularly well for compiling large quantum circuits at the same time, as opposed to the [Jabalizer](https://github.com/QSI-BAQS/Jabalizer.jl) tool, which breaks the circuit up into smaller pieces. Unfortunately, because making the widgets includes a significant amount of overhead, this tool is not well suited for compiling small circuits. It also produces ASGs of lower quality than Jabalizer. The main advantage of this package is the sheer number of available compilation options. We will cover these in detail below.

## Installation

As noted in the main README of BenchQ, you must first install the [Julia](https://julialang.org/) programming language in order to perform compilation. Here we have implemented some simple code which automatically installs Julia if we cannot find it on your system. This is fast and simple to use, but might irk some users. If you would like to install Julia yourself, you can do so by following the instructions [here](https://julialang.org/downloads/).

## Options

The python interface for this package is generated allows for a number of options to be set when running a compilation. These options can be broadly split up into two catagories: Ruby Slippers hyperparameters and Pauli Tracking parameters.


### Table Generation

The graph state simulator I use required generating several tables which can be found in `graph_sim_data.jl`. The code which generated these tables can be found in the `table_generation` folder.

TODOs:
[ ] - Set up pythonic interface
[ ] - Improve and run testing
[ ] - Set up native julia testing that is called via python
[ ] - Make ruby slippers take in orquestra circuits

