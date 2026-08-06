# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# check availability
hdf5.available := ${findstring hdf5,$(extern.available)}

# if {hdf5} is available
ifeq ($(hdf5.available), hdf5)


# h5 ships no python package of its own; its python lives in {packages/pyre/h5}, part of {pyre.pkg}
pyre-h5.packages :=
# a library
pyre-h5.libraries := pyre-h5.lib
# a python extension, deposited into the {pyre} package that hosts it
pyre-h5.extensions := pyre-h5.ext
# a c++ test suite (like {pyre::postgres} the library stands on its own, apart from {libpyre})
# and a python test suite for the bindings
pyre-h5.tests := pyre-h5.lib.tests pyre-h5.ext.tests


# the h5 library meta-data
pyre-h5.lib.root := lib/h5/
pyre-h5.lib.stem := pyre-h5
# deposit the headers under the {pyre} namespace so they never collide in a shared prefix
pyre-h5.lib.incdir := $(builder.dest.inc)pyre/h5/
# the gateway header is deposited one level above the rest, as {pyre/h5.h}
pyre-h5.lib.gateway := h5.h
pyre-h5.lib.prerequisites := pyre.lib journal.lib
pyre-h5.lib.extern := pyre.lib journal.lib hdf5
pyre-h5.lib.c++.flags += $(pyre.lib.c++.flags)
pyre-h5.lib.c++.defines += $(pyre.lib.c++.defines)

# the h5 extension meta-data; it wraps the library above
pyre-h5.ext.root := extensions/h5/
# the module stays {h5}; {packages/pyre/extensions} re-exports it as {libh5}
pyre-h5.ext.stem := h5
# the module rides in the {pyre} package, alongside {libpyre}
pyre-h5.ext.pkg := pyre.pkg
pyre-h5.ext.wraps := pyre-h5.lib
# the bindings hand back real classes now, so there are no capsule headers to publish
pyre-h5.ext.capsule :=
pyre-h5.ext.lib.prerequisites := pyre-h5.lib pyre.lib
pyre-h5.ext.extern := pyre.lib journal.lib hdf5 pybind11 python
pyre-h5.ext.lib.c++.flags += $(pyre-h5.lib.c++.flags)
pyre-h5.ext.lib.c++.defines += $(pyre-h5.lib.c++.defines)


# get the testsuites
include pyre-h5.lib.tests pyre-h5.ext.tests


endif


# end of file
