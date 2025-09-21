# configs/common_simple_sys.py
from m5.objects import *

# Minimal cache helpers (classic memory system)
class L1_ICache(Cache):
    assoc = 2
    tag_latency = 2
    data_latency = 2
    response_latency = 2
    mshrs = 16
    tgts_per_mshr = 8
    size = '32kB'
    is_read_only = True
    def connectCPU(self, cpu):
        self.cpu_side = cpu.icache_port
    def connectBus(self, bus):
        self.mem_side = bus.cpu_side_ports

class L1_DCache(Cache):
    assoc = 2
    tag_latency = 2
    data_latency = 2
    response_latency = 2
    mshrs = 16
    tgts_per_mshr = 8
    size = '32kB'
    def connectCPU(self, cpu):
        self.cpu_side = cpu.dcache_port
    def connectBus(self, bus):
        self.mem_side = bus.cpu_side_ports

class L2Cache(Cache):
    assoc = 8
    tag_latency = 20
    data_latency = 20
    response_latency = 20
    mshrs = 32
    tgts_per_mshr = 16
    size = '1MB'
    def connectCPUSideBus(self, bus):
        self.cpu_side = bus.mem_side_ports
    def connectMemSideBus(self, bus):
        self.mem_side = bus.cpu_side_ports

def make_simple_system(cpu, mem_size="512MB", clk="3GHz", workload_path="/bin/true"):
    system = System()
    system.clk_domain = SrcClockDomain(clock=clk, voltage_domain=VoltageDomain())
    system.mem_mode = 'timing'
    system.mem_ranges = [AddrRange(mem_size)]

    system.membus = SystemXBar(width=64)

    # DRAM
    system.mem_ctrl = MemCtrl()
    system.mem_ctrl.dram = DDR3_1600_8x8()
    system.mem_ctrl.dram.range = system.mem_ranges[0]
    system.mem_ctrl.port = system.membus.mem_side_ports

    # CPU + private L1s, shared L2
    system.cpu = cpu
    system.cpu.icache = L1_ICache()
    system.cpu.dcache = L1_DCache()
    system.cpu.icache.connectCPU(system.cpu)
    system.cpu.dcache.connectCPU(system.cpu)

    system.l2bus = L2XBar(width=64)
    system.cpu.icache.connectBus(system.l2bus)
    system.cpu.dcache.connectBus(system.l2bus)

    system.l2cache = L2Cache()
    system.l2cache.connectCPUSideBus(system.l2bus)
    system.l2cache.connectMemSideBus(system.membus)

    # Interrupts (x86)
    if hasattr(system.cpu, 'createInterruptController'):
        system.cpu.createInterruptController()

    # SE mode workload must be initialized with a *path* (positional)
    system.workload = SEWorkload.init_compatible(workload_path)

    # System port
    system.system_port = system.membus.cpu_side_ports
    return system

