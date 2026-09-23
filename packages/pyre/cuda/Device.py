# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


class Device:
    """
    The property sheet of a CUDA capable device
    """

    # attributes
    id = None
    name = ""

    capability = ()
    driverVersion = ()
    runtimeVersion = ()
    computeMode = 0

    managedMemory = False
    unifiedAddressing = False

    processors = 0
    coresPerProcessor = 0

    globalMemory = 0
    constantMemory = 0
    sharedMemoryPerBlock = 0

    warp = 0
    maxThreadsPerBlock = 0
    maxThreadsPerProcessor = 0

    maxGrid = ()
    maxThreadBlock = ()

    # the cublas/cusolver/curand handles bound to this device, allocated once and reused for
    # as long as the process runs; a simulation that calls into cublas every step would
    # otherwise pay for a fresh handle on every call, which is wasted work against the same
    # device for the same duration
    _cublasHandle = None
    _cusolverHandle = None
    _curandGenerator = None

    # handles
    @property
    def cublasHandle(self):
        """
        The cublas handle bound to this device, created on first use and cached from then on
        """
        # if this is the first request
        if self._cublasHandle is None:
            # make sure the handle binds to this device, not whichever one happened to be
            # current
            self._activate()
            # pull in the bindings lazily, so importing this module doesn't require cuda
            import pyre.cuda

            # make the handle
            self._cublasHandle = pyre.cuda.cublas.create()
        # hand it back
        return self._cublasHandle

    @property
    def cusolverHandle(self):
        """
        The cusolverDn handle bound to this device, created on first use and cached from then
        on
        """
        if self._cusolverHandle is None:
            self._activate()
            import pyre.cuda

            self._cusolverHandle = pyre.cuda.cusolver.create()
        return self._cusolverHandle

    def curandGenerator(self, rngType=None):
        """
        The curand generator bound to this device, created on first use and cached from then
        on; {rngType} only matters the first time this is called, since later calls hand back
        the same generator regardless
        """
        if self._curandGenerator is None:
            self._activate()
            import pyre.cuda

            rngType = pyre.cuda.curand.RngType.DEFAULT if rngType is None else rngType
            self._curandGenerator = pyre.cuda.curand.create_generator(rngType)
        return self._curandGenerator

    # implementation details
    def _activate(self):
        """
        Make this the current device, so a handle allocated against it binds to the right one
        """
        # pull in {cuda.core} lazily, for the same reason as above
        import cuda.core

        cuda.core.Device(self.id).set_current()
        # all done
        return

    # debugging
    def dump(self, indent=""):
        """
        Print information about this device
        """
        print(f"{indent}device {self.id}:")
        print(f"{indent}  name: {self.name}")

        print(f"{indent}  driver version: {self.driverVersion}")
        print(f"{indent}  runtime version: {self.runtimeVersion}")
        print(f"{indent}  compute capability: {self.capability}")
        print(f"{indent}  compute mode: {self.computeMode}")

        print(f"{indent}  managed memory: {self.managedMemory}")
        print(f"{indent}  unified addressing: {self.unifiedAddressing}")

        print(f"{indent}  processors: {self.processors}")
        print(f"{indent}  cores per processor: {self.coresPerProcessor}")

        print(f"{indent}  global memory: {self.globalMemory} bytes")
        print(f"{indent}  constant memory: {self.constantMemory} bytes")
        print(f"{indent}  shared memory per block: {self.sharedMemoryPerBlock} bytes")

        print(f"{indent}  warp: {self.warp} threads")
        print(f"{indent}  max threads per block: {self.maxThreadsPerBlock}")
        print(f"{indent}  max threads per processor: {self.maxThreadsPerProcessor}")

        print(f"{indent}  max dimensions of a grid: {self.maxGrid}")
        print(f"{indent}  max dimensions of a thread block: {self.maxThreadBlock}")

        # all done
        return


# end of file
