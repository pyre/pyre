# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# check availability
pyre-cuda.cuda.available := ${findstring cuda,$(extern.available)}

# the cuda aware parts of the {pyre} extension: the thin cublas/cusolver/curand bindings under
# {cuda/}, and the device half of in-place grid arithmetic; the rest of the extension carries
# its cuda support behind {WITH_CUDA}
pyre.ext.cuda.sources = $(pyre.ext.lib.prefix)grid/arithmetic_device.cu

# if cuda is available
ifeq ($(pyre-cuda.cuda.available), cuda)

# pyre-cuda builds a python package
pyre-cuda.packages := pyre-cuda.pkg
# and a header only library
pyre-cuda.libraries := pyre-cuda.lib
# its bindings live in the {pyre} extension, so it has none of its own
pyre-cuda.extensions :=

# building {pyre-cuda} needs only the cuda toolkit, but running its tests needs an actual
# device to execute on; gate the test suites on the presence of a cuda runtime, not on the
# build-time availability of the package; probe the driver with {nvidia-smi} — the canonical
# check, since the {/dev/nvidia*} nodes can be absent on a capable host until the driver
# initializes them — but let the user override
pyre-cuda.cuda.runtime ?= ${if ${shell command -v nvidia-smi > /dev/null 2>&1 && nvidia-smi -L 2>/dev/null | grep -m1 '^GPU'},cuda,}
ifeq ($(pyre-cuda.cuda.runtime), cuda)
pyre-cuda.tests := pyre-cuda.pkg.tests pyre-cuda.lib.tests
else
pyre-cuda.tests :=
endif

# the package lives under the {pyre} namespace, as {pyre.cuda}, so it doesn't collide with
# nvidia's own {cuda-python}, which claims the top level {cuda}; it is a package of its own,
# rather than part of {pyre.pkg}, because it carries its own meta-data; device discovery is
# pure python, riding on nvidia's {cuda.bindings}/{cuda.core}
pyre-cuda.pkg.root := packages/pyre/cuda/
pyre-cuda.pkg.stem := cuda
pyre-cuda.pkg.name := pyre/cuda
pyre-cuda.pkg.ext :=

# the library
pyre-cuda.lib.root := lib/cuda/
pyre-cuda.lib.stem := pyre-cuda
pyre-cuda.lib.incdir := $(builder.dest.inc)pyre/cuda/
pyre-cuda.lib.languages := c++ cuda
pyre-cuda.lib.prerequisites := journal.lib pyre.lib
pyre-cuda.lib.extern := pyre.lib pyre cuda
pyre-cuda.lib.c++.flags += $(pyre.lib.c++.flags)
pyre-cuda.lib.c++.defines += $(pyre.lib.c++.defines)
pyre-cuda.lib.cuda.flags += $(nvcc.std.c++17)
pyre-cuda.lib.cuda.defines += $(pyre.lib.c++.defines)

# the {pyre} extension grows its cuda aware parts: {grid.managed}, the cuda array interface,
# in-place arithmetic on the device, and the {cuda} submodule; they need the toolkit, the
# cuda storage headers, and the compile time flag, in both the c++ and the cuda sources
pyre.ext.extern += cuda
pyre.ext.lib.prerequisites += pyre-cuda.lib
pyre.ext.lib.c++.defines += WITH_CUDA
pyre.ext.lib.cuda.defines += WITH_CUDA $(pyre.lib.c++.defines)
pyre.ext.lib.cuda.flags += $(nvcc.std.c++20)

# cuda configuration: make sure linking includes these libraries
cuda.libraries += cudart cublas cusolver curand

# get the testsuites, when a cuda runtime gated them in
ifeq ($(pyre-cuda.cuda.runtime), cuda)
include $(pyre-cuda.tests)
endif

# if cuda is not available
else

# leave the cuda aware parts out of the {pyre} extension
pyre.ext.lib.directories.exclude += cuda
pyre.ext.lib.sources.exclude += $(pyre.ext.cuda.sources)

endif


# end of file
