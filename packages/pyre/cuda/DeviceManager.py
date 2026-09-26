# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# meta-class
from pyre.patterns.Singleton import Singleton
# the exceptions this package raises
from .exceptions import Error

# nvidia's own cuda python bindings; device discovery, selection, and properties all come
# from here now, instead of a hand rolled cuda runtime api wrapper
from cuda.bindings import runtime as cudart
import cuda.core


# the number of cores per streaming multiprocessor, indexed by (major, minor) compute
# capability; cuda-python doesn't publish this, since it isn't a runtime-queryable property,
# so a lookup table is the only way to get it, exactly as before
_coresPerProcessor = {
    (0xC, 0x1): 128,  # GB10l           (SM 12.1) DGX Spark (to verify...)
    (0xC, 0x0): 128,  # RTX Blackwell   (SM 12.0) RTX
    (0xA, 0x3): 128,  # Blackwell Ultra (SM 10.3) B300 / GB300
    (0xA, 0x0): 128,  # Blackwell       (SM 10.0) B200 / GB200
    (0x9, 0x0): 128,  # Hopper          (SM  9.0) H100 / H200 / GH200
    (0x8, 0x9): 128,  # Ada             (SM  8.9) RTX 40, L4/L40
    (0x8, 0x7): 128,  # Ampere          (SM  8.7) Jetson Orin
    (0x8, 0x6): 128,  # Ampere          (SM  8.6) GA10x
    (0x8, 0x0): 64,   # Ampere          (SM  8.0) GA100
    (0x7, 0x5): 64,   # Turing          (SM  7.5) TU10x
    (0x7, 0x2): 64,   # Volta           (SM  7.2) GV100
    (0x7, 0x0): 64,   # Volta           (SM  7.0) GV100
    (0x6, 0x2): 128,  # Pascal          (SM  6.2) GP10x
    (0x6, 0x1): 128,  # Pascal          (SM  6.1) GP10x
    (0x6, 0x0): 64,   # Pascal          (SM  6.0) GP100
    (0x5, 0x3): 128,  # Maxwell         (SM  5.3) GM20x
    (0x5, 0x2): 128,  # Maxwell         (SM  5.2) GM20x
    (0x5, 0x0): 128,  # Maxwell         (SM  5.0) GM10x
    (0x3, 0x7): 192,  # Kepler          (SM  3.7) GK21x
    (0x3, 0x5): 192,  # Kepler          (SM  3.5) GK11x
    (0x3, 0x2): 192,  # Kepler          (SM  3.2) GK10x
    (0x3, 0x0): 192,  # Kepler          (SM  3.0) GK10x
}


def _check(outcome):
    """
    {cuda.bindings.runtime} calls return {(cudaError_t, *values)}, the c api's own
    convention, rather than raising on failure; check the status and unpack the rest
    """
    # split the status from whatever else the call returned
    status, *values = outcome
    # if the call failed
    if status != cudart.cudaError_t.cudaSuccess:
        # find out what the runtime has to say about it
        _, name = cudart.cudaGetErrorName(status)
        # and complain
        raise Error(description=f"cuda error: {name} ({int(status)})")
    # unpack the singleton case, so a caller of a single-value function doesn't have to
    if len(values) == 1:
        return values[0]
    # otherwise hand back whatever there was, packed as a tuple
    return tuple(values)


def _coreCount(major, minor):
    """
    Look up the number of cores per streaming multiprocessor for the given compute capability
    """
    # attempt to
    try:
        # find it in the table
        return _coresPerProcessor[(major, minor)]
    # if this generation isn't in the table
    except KeyError:
        # the table is out of date; don't fail the whole discovery over it
        import journal

        journal.firewall("cuda").log(f"core count for generation ({major},{minor}) is unknown")
        return 0


def _sheet(factory, device):
    """
    Build a {factory} instance (typically a {Device} property sheet) describing the given
    {cuda.core.Device}
    """
    # make the sheet
    sheet = factory()
    # its properties
    props = device.properties
    # the driver/runtime versions, split into (major, minor) the way the old c extension did
    driver = _check(cudart.cudaDriverGetVersion())
    runtime = _check(cudart.cudaRuntimeGetVersion())

    # decorate
    sheet.id = device.device_id
    sheet.name = device.name
    sheet.capability = (device.compute_capability.major, device.compute_capability.minor)
    sheet.driverVersion = (driver // 1000, (driver % 100) // 10)
    sheet.runtimeVersion = (runtime // 1000, (runtime % 100) // 10)
    sheet.computeMode = props.compute_mode
    sheet.managedMemory = bool(props.managed_memory)
    sheet.unifiedAddressing = bool(props.unified_addressing)
    sheet.processors = props.multiprocessor_count
    sheet.coresPerProcessor = _coreCount(device.compute_capability.major, device.compute_capability.minor)
    sheet.constantMemory = props.total_constant_memory
    sheet.sharedMemoryPerBlock = props.max_shared_memory_per_block
    sheet.warp = props.warp_size
    sheet.maxThreadsPerBlock = props.max_threads_per_block
    sheet.maxThreadsPerProcessor = props.max_threads_per_multiprocessor
    sheet.maxGrid = (props.max_grid_dim_x, props.max_grid_dim_y, props.max_grid_dim_z)
    sheet.maxThreadBlock = (props.max_block_dim_x, props.max_block_dim_y, props.max_block_dim_z)

    # total global memory isn't one of the queryable properties; it comes from its own call,
    # and only for whichever device is currently active
    device.set_current()
    sheet.globalMemory = _check(cudart.cudaMemGetInfo())[1]

    # all done
    return sheet


# declaration
class DeviceManager(metaclass=Singleton):
    """
    The singleton that provides access to what is known about CUDA capable hardware
    """

    # public data
    count = 0
    devices = []

    # interface
    def device(self, did=0):
        """
        Set {did} as the current device
        """
        # delegate to cuda.core
        return cuda.core.Device(did).set_current()

    def reset(self):
        """
        Reset the current device
        """
        # delegate to the runtime bindings
        return _check(cudart.cudaDeviceReset())

    # meta-methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)

        # grab the device sheet class
        from .Device import Device

        # discover the attached devices and build a property sheet for each
        self.devices = [
            _sheet(Device, device) for device in cuda.core.Device.get_all_devices()
        ]
        # set the count
        self.count = len(self.devices)

        # all done
        return


# end of file
