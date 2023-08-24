"""
Usage
-----

```
scons build/ARM/gem5.opt
./build/ARM/gem5.opt configs/example/gem5_library/arm-simpoint-benchmarks.py
```
"""

import argparse
from gem5.isas import ISA
from gem5.components.processors.cpu_types import (
    get_cpu_types_str_set,
    get_cpu_type_from_str,
)
from gem5.utils.requires import requires
from gem5.resources.resource import BinaryResource
from gem5.components.memory import SingleChannelDDR3_1600
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.base_cpu_core import BaseCPUCore
from gem5.components.processors.base_cpu_processor import BaseCPUProcessor
from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.no_cache import NoCache
from gem5.simulate.simulator import Simulator
from gem5.isas import get_isa_from_str, get_isas_str_set
from m5.objects import ArmNonCachingSimpleCPU

# This check ensures the gem5 binary is compiled to the ARM ISA target. If not,
# an exception will be thrown.
requires(isa_required=ISA.ARM)

parser = argparse.ArgumentParser(
    description="A gem5 script for running ARM simpoint benchmarks in SE mode."
)

parser.add_argument(
    "-c", "--cmd", type=str, help="The binary to run in syscall emulation mode."
)

parser.add_argument(
    "--arguments",
    type=str,
    action="append",
    default=[],
    required=False,
    help="The input arguments for the binary.",
)

# Simpoint options
parser.add_argument(
    "--simpoint-profile",
    action="store_true",
    help="Enable basic block profiling for SimPoints",
)

parser.add_argument(
    "--simpoint-interval",
    type=int,
    default=10000000,
    help="SimPoint interval in num of instructions",
)

args = parser.parse_args()

cache_hierarchy = NoCache()
memory = SingleChannelDDR3_1600()
cpu = ArmNonCachingSimpleCPU()
if args.simpoint_profile:
    cpu.addSimPointProbe(args.simpoint_interval)
core = BaseCPUCore(core=cpu, isa=get_isa_from_str("arm"))
processor = BaseCPUProcessor(cores=[core])

board = SimpleBoard(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)

binary = BinaryResource(local_path=args.cmd)
board.set_se_binary_workload(binary, arguments=args.arguments)

# Lastly we run the simulation.
simulator = Simulator(board=board)
simulator.run()

print(
    "Exiting @ tick {} because {}.".format(
        simulator.get_current_tick(), simulator.get_last_exit_event_cause()
    )
)
