# configs/part2_branch_pred_minor.py
import os, sys, argparse
sys.path.append(os.path.dirname(__file__))

from m5.objects import *
from common_simple_sys import make_simple_system

parser = argparse.ArgumentParser()
parser.add_argument("--binary", required=True)
parser.add_argument("--pred", choices=["none","local","tournament","bi"], default="local")
parser.add_argument("--clk", default="3GHz")
parser.add_argument("--mem", default="512MB")
args = parser.parse_args()

# robust MinorCPU init
try:
    cpu = MinorCPU()
except TypeError:
    from m5.objects import MinorCPU as MinorCPU_mod
    cpu = MinorCPU_mod.MinorCPU()

# choose predictor when the attribute exists
if hasattr(cpu, "branchPred"):
    if args.pred == "none":
        cpu.branchPred = NullBP()
    elif args.pred == "local":
        cpu.branchPred = LocalBP()
    elif args.pred == "tournament":
        cpu.branchPred = TournamentBP()
    elif args.pred == "bi":
        cpu.branchPred = BiModeBP()

system = make_simple_system(cpu, mem_size=args.mem, clk=args.clk)

p = Process()
p.cmd = [args.binary]
system.cpu.workload = p
system.cpu.createThreads()

root = Root(full_system=False, system=system)

