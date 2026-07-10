# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# check availability
pyre-gsl.gsl.available := ${findstring gsl,$(extern.available)}
pyre-gsl.mpi.available := ${findstring mpi,$(extern.available)}

# if {gsl} is available
ifeq ($(pyre-gsl.gsl.available), gsl)


# gsl builds a python package
pyre-gsl.packages := pyre-gsl.pkg
# no library
pyre-gsl.libraries :=
# a python extension
pyre-gsl.extensions := pyre-gsl.ext
# and test suites
pyre-gsl.tests := pyre-gsl.pkg.tests


# the gsl package meta-data
pyre-gsl.pkg.root := packages/gsl/
pyre-gsl.pkg.stem := gsl
pyre-gsl.pkg.meta :=
pyre-gsl.pkg.ext :=

# the gsl extension meta-data
pyre-gsl.ext.root := extensions/gsl/
# the module is {libgsl}, so that it does not shadow the {gsl} package that hosts it, and so
# that it reads like its siblings {libpyre} and {libmpi}
pyre-gsl.ext.stem := libgsl
pyre-gsl.ext.pkg := pyre-gsl.pkg
pyre-gsl.ext.wraps :=
pyre-gsl.ext.capsule.destination := pyre/gsl/
pyre-gsl.ext.lib.prerequisites := journal.lib pyre.lib
pyre-gsl.ext.extern := pyre.lib journal.lib gsl
pyre-gsl.ext.lib.c++.flags += $(pyre.lib.c++.flags)
pyre-gsl.ext.lib.c++.defines += $(pyre.lib.c++.defines)

#
# adjustments that depend on  the availability of external dependencies
#

# if we have mpi
ifeq ($(pyre-gsl.mpi.available), mpi)
# add mpi to the external dependencies
pyre-gsl.ext.extern += mpi
# the partitioning code takes communicators straight out of the {libmpi} bindings, so it needs
# the declarations in {pyre::mpi}; the module itself is no longer a build time dependency, now
# that there are no capsules for it to export
pyre-gsl.ext.lib.prerequisites += pyre-mpi.lib
# if not
else
# remove the mpi dependent sources from the build
pyre-gsl.ext.lib.sources.exclude += $(pyre-gsl.ext.lib.prefix)partition.cc
endif

# unconditionally add python and pybind11 to the external libraries
pyre-gsl.ext.extern += python pybind11


# get the testsuites
include pyre-gsl.pkg.tests


endif


# end of file
