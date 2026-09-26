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

    # the library handles bound to this device, made on first use and reused after that
    _cublasHandle = None
    _cusolverHandle = None
    _curandGenerator = None

    # handles
    @property
    def cublasHandle(self) -> int:
        """
        The cublas handle bound to this device
        """
        # on first use
        if self._cublasHandle is None:
            # the bindings
            import pyre.cuda

            # make sure the handle binds to this device
            self._activate()
            # and make it
            self._cublasHandle = pyre.cuda.cublas.create()
        # hand off the handle
        return self._cublasHandle

    @property
    def cusolverHandle(self) -> int:
        """
        The cusolver handle bound to this device
        """
        # on first use
        if self._cusolverHandle is None:
            # the bindings
            import pyre.cuda

            # make sure the handle binds to this device
            self._activate()
            # and make it
            self._cusolverHandle = pyre.cuda.cusolver.create()
        # hand off the handle
        return self._cusolverHandle

    def curandGenerator(self, rngType=None) -> int:
        """
        The curand generator bound to this device; {rngType} picks its kind the first time only
        """
        # on first use
        if self._curandGenerator is None:
            # the bindings
            import pyre.cuda

            # make sure the generator binds to this device
            self._activate()
            # the kind of generator, the default one unless asked otherwise
            kind = pyre.cuda.curand.RngType.DEFAULT if rngType is None else rngType
            # make it
            self._curandGenerator = pyre.cuda.curand.create_generator(kind)
        # hand off the generator
        return self._curandGenerator

    # implementation details
    def _activate(self) -> None:
        """
        Make this the current device
        """
        # cuda-python
        import cuda.core

        # select the device
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
