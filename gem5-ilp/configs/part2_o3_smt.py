from m5.objects import *
from common_simple_sys import make_simple_system
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--binaries", nargs='+', required=True, help="Two binaries for SMT")
parser.add_argument("--width", type=int, default=4)
parser.add_argument("--threads", type=int, default=2)
parser.add_argument("--clk", default="3GHz")
parser.add_argument("--mem", default="512MB")
args = parser.parse_args()

cpu = DerivO3CPU()
cpu.fetchWidth  = args.width
cpu.decodeWidth = args.width
cpu.renameWidth = args.width
cpu.issueWidth  = args.width
cpu.executeWidth= args.width
cpu.commitWidth = args.width
cpu.numThreads = args.threads

cpu.branchPred = TournamentBP()

system = make_simple_system(cpu, mem_size=args.mem, clk=args.clk)

procs = []
for b in args.binaries[:args.threads]:
    p = Process()
    p.cmd = [b]
    procs.append(p)

system.cpu.workload = procs
system.cpu.createThreads()

root = Root(full_system=False, system=system)

