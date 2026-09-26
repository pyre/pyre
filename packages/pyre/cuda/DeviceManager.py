# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import typing

# cuda-python
import cuda.core
from cuda.bindings import runtime as cudart

# framework
import journal
from pyre.patterns.Singleton import Singleton

# local
from .exceptions import Error

# the number of cores per streaming multiprocessor, by compute capability; the runtime does not
# report it, so it comes from this table
_coresPerProcessor = {
    (0xC, 0x1): 128,  # GB10l           (SM 12.1) DGX Spark
    (0xC, 0x0): 128,  # RTX Blackwell   (SM 12.0) RTX
    (0xA, 0x3): 128,  # Blackwell Ultra (SM 10.3) B300 / GB300
    (0xA, 0x0): 128,  # Blackwell       (SM 10.0) B200 / GB200
    (0x9, 0x0): 128,  # Hopper          (SM  9.0) H100 / H200 / GH200
    (0x8, 0x9): 128,  # Ada             (SM  8.9) RTX 40, L4/L40
    (0x8, 0x7): 128,  # Ampere          (SM  8.7) Jetson Orin
    (0x8, 0x6): 128,  # Ampere          (SM  8.6) GA10x
    (0x8, 0x0): 64,  # Ampere          (SM  8.0) GA100
    (0x7, 0x5): 64,  # Turing          (SM  7.5) TU10x
    (0x7, 0x2): 64,  # Volta           (SM  7.2) GV100
    (0x7, 0x0): 64,  # Volta           (SM  7.0) GV100
    (0x6, 0x2): 128,  # Pascal          (SM  6.2) GP10x
    (0x6, 0x1): 128,  # Pascal          (SM  6.1) GP10x
    (0x6, 0x0): 64,  # Pascal          (SM  6.0) GP100
    (0x5, 0x3): 128,  # Maxwell         (SM  5.3) GM20x
    (0x5, 0x2): 128,  # Maxwell         (SM  5.2) GM20x
    (0x5, 0x0): 128,  # Maxwell         (SM  5.0) GM10x
    (0x3, 0x7): 192,  # Kepler          (SM  3.7) GK21x
    (0x3, 0x5): 192,  # Kepler          (SM  3.5) GK11x
    (0x3, 0x2): 192,  # Kepler          (SM  3.2) GK10x
    (0x3, 0x0): 192,  # Kepler          (SM  3.0) GK10x
}


def _check(outcome: tuple) -> typing.Any:
    """
    Check the status of a runtime call and unpack the values it returned in {outcome}
    """
    # split the status from the values
    status, *values = outcome
    # if the call failed
    if status != cudart.cudaError_t.cudaSuccess:
        # ask the runtime for the name of the error
        _, name = cudart.cudaGetErrorName(status)
        # and complain
        raise Error(description=f"cuda error: {name.decode()} ({int(status)})")
    # a single value is handed back by itself
    if len(values) == 1:
        # so unpack it
        return values[0]
    # anything else, as a tuple
    return tuple(values)


def _coreCount(major: int, minor: int) -> int | None:
    """
    The number of cores per streaming multiprocessor of compute capability {major}.{minor}
    """
    # look it up
    cores = _coresPerProcessor.get((major, minor))
    # a generation the table does not know
    if cores is None:
        # is a gap in the table
        journal.firewall("pyre.cuda.discovery").log(
            f"the core count of compute capability {major}.{minor} is unknown"
        )
    # hand off the count
    return cores


def _sheet(factory: type, device: cuda.core.Device) -> typing.Any:
    """
    Build a {factory} instance that describes {device}
    """
    # make the sheet
    sheet = factory()
    # the properties of the device
    props = device.properties
    # the version of the driver
    driver = _check(cudart.cudaDriverGetVersion())
    # and of the runtime
    runtime = _check(cudart.cudaRuntimeGetVersion())
    # the capability of the device
    capability = device.compute_capability
    # its ordinal
    sheet.id = device.device_id
    # its name
    sheet.name = device.name
    # its compute capability
    sheet.capability = (capability.major, capability.minor)
    # the version of the driver, as a {(major, minor)} pair
    sheet.driverVersion = (driver // 1000, (driver % 100) // 10)
    # and of the runtime
    sheet.runtimeVersion = (runtime // 1000, (runtime % 100) // 10)
    # its compute mode
    sheet.computeMode = props.compute_mode
    # whether it supports managed memory
    sheet.managedMemory = bool(props.managed_memory)
    # whether it shares an address space with the host
    sheet.unifiedAddressing = bool(props.unified_addressing)
    # the number of streaming multiprocessors
    sheet.processors = props.multiprocessor_count
    # the number of cores in each
    sheet.coresPerProcessor = _coreCount(capability.major, capability.minor)
    # the amount of constant memory
    sheet.constantMemory = props.total_constant_memory
    # the amount of shared memory per block
    sheet.sharedMemoryPerBlock = props.max_shared_memory_per_block
    # the width of a warp
    sheet.warp = props.warp_size
    # the most threads in a block
    sheet.maxThreadsPerBlock = props.max_threads_per_block
    # the most threads on a streaming multiprocessor
    sheet.maxThreadsPerProcessor = props.max_threads_per_multiprocessor
    # the largest grid
    sheet.maxGrid = (props.max_grid_dim_x, props.max_grid_dim_y, props.max_grid_dim_z)
    # the largest block
    sheet.maxThreadBlock = (props.max_block_dim_x, props.max_block_dim_y, props.max_block_dim_z)
    # the amount of global memory comes from the current device
    device.set_current()
    # so ask for it
    sheet.globalMemory = _check(cudart.cudaMemGetInfo())[1]
    # hand off the sheet
    return sheet


class DeviceManager(metaclass=Singleton):
    """
    The singleton that knows the cuda capable hardware attached to this machine
    """

    # public data
    count = 0
    devices = []

    # interface
    def device(self, did: int = 0) -> None:
        """
        Make the device with ordinal {did} the current one
        """
        # delegate to cuda-python
        cuda.core.Device(did).set_current()
        # all done
        return

    def reset(self) -> None:
        """
        Reset the current device
        """
        # delegate to the runtime
        _check(cudart.cudaDeviceReset())
        # all done
        return

    # metamethods
    def __init__(self, **kwds):
        """
        Discover the attached devices
        """
        # chain up
        super().__init__(**kwds)
        # the class of the property sheets
        from .Device import Device

        # describe each attached device
        self.devices = [_sheet(Device, device) for device in cuda.core.Device.get_all_devices()]
        # and count them
        self.count = len(self.devices)
        # all done
        return


# end of file
