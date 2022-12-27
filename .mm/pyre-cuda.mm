# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


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
# and test suites
pyre-cuda.tests := pyre-cuda.pkg.tests pyre-cuda.lib.tests


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
pyre-cuda.lib.c++.flags += $($(compiler.c++).std.c++17)
pyre-cuda.lib.cuda.flags += $(nvcc.std.c++17)

# the extension
pyre-cuda.ext.root := extensions/cuda/
pyre-cuda.ext.stem := cuda
pyre-cuda.ext.pkg := pyre-cuda.pkg
pyre-cuda.ext.wraps :=
pyre-cuda.ext.capsule :=
pyre-cuda.ext.extern := pyre.lib journal.lib cuda python
pyre-cuda.ext.lib.c++.flags += $($(compiler.c++).std.c++17)
pyre-cuda.ext.lib.prerequisites += journal.lib pyre.lib

# cuda configuration: make sure linking includes these libraries
cuda.libraries += cudart


# get the testsuites
include $(pyre-cuda.tests)


endif


# end of file
