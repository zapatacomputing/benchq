from benchq.data_structures import SubroutineModel

from benchq.algorithms.ld_gsee import (
    get_ff_ld_gsee_max_evolution_time,
    get_ff_ld_gsee_num_circuit_repetitions,
    LD_GSEE,
)
from benchq.algorithms.time_evolution import (
    QSPTimeEvolution,
)

# Create an instance of QSPTimeEvolution
c_time_evolution = QSPTimeEvolution()

# Create an instance of LD_GSEE with QSPTimeEvolution as a task
ld_gsee = LD_GSEE(c_time_evolution=c_time_evolution)

# Set the requirements for LD_GSEE
ld_gsee.set_requirements(
    alpha=0.5,
    energy_gap=0.3,
    square_overlap=0.8,
    precision=0.001,
    failure_tolerance=0.1,
    hamiltonian="H",
)

# Run the profile
ld_gsee.run_profile()

# Print the profile
ld_gsee.print_profile()

# Count the subroutines
print(ld_gsee.count_subroutines())
