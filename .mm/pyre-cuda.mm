# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# check availability
pyre-cuda.cuda.available := ${findstring cuda,$(extern.available)}

# if cuda is available
ifeq ($(pyre-cuda.cuda.available), cuda)


# pyre-cuda builds a python package
pyre-cuda.packages := pyre-cuda.pkg
# no libraries
pyre-cuda.libraries := pyre-cuda.lib
# the mandatory extensions
pyre-cuda.extensions := pyre-cuda.ext

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


# the package
pyre-cuda.pkg.root := packages/cuda/
pyre-cuda.pkg.stem := cuda
pyre-cuda.pkg.meta :=
pyre-cuda.pkg.ext :=

# the library
pyre-cuda.lib.root := lib/cuda/
pyre-cuda.lib.stem := pyre_cuda
pyre-cuda.lib.incdir := $(builder.dest.inc)pyre/cuda/
pyre-cuda.lib.languages := c++ cuda
pyre-cuda.lib.prerequisites := journal.lib pyre.lib
pyre-cuda.lib.extern := pyre.lib pyre cuda
pyre-cuda.lib.c++.flags += $(pyre.lib.c++.flags)
pyre-cuda.lib.c++.defines += $(pyre.lib.c++.defines)
pyre-cuda.lib.cuda.flags += $(nvcc.std.c++17)
pyre-cuda.lib.cuda.defines += $(pyre.lib.c++.defines)

# the extension
pyre-cuda.ext.root := extensions/cuda/
pyre-cuda.ext.stem := cuda
pyre-cuda.ext.pkg := pyre-cuda.pkg
pyre-cuda.ext.wraps :=
pyre-cuda.ext.capsule :=
pyre-cuda.ext.extern := pyre.lib journal.lib cuda python
pyre-cuda.ext.lib.c++.flags += $(pyre-cuda.lib.c++.flags)
pyre-cuda.ext.lib.c++.defines += $(pyre-cuda.lib.c++.defines)
pyre-cuda.ext.lib.prerequisites += journal.lib pyre.lib

# cuda configuration: make sure linking includes these libraries
cuda.libraries += cudart


# get the testsuites, when a cuda runtime gated them in
ifeq ($(pyre-cuda.cuda.runtime), cuda)
include $(pyre-cuda.tests)
endif


endif


# end of file
