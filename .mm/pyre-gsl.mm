# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# check availability
pyre-gsl.gsl.available := ${findstring gsl,$(extern.available)}
pyre-gsl.mpi.available := ${findstring mpi,$(extern.available)}
pyre-gsl.numpy.available := ${findstring numpy,$(extern.available)}

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
pyre-gsl.ext.stem := gsl
pyre-gsl.ext.pkg := pyre-gsl.pkg
pyre-gsl.ext.wraps :=
pyre-gsl.ext.capsule.destination := pyre/gsl/
pyre-gsl.ext.lib.prerequisites := journal.lib pyre.lib
pyre-gsl.ext.extern := pyre.lib journal.lib gsl
pyre-gsl.ext.lib.c++.flags += $($(compiler.c++).std.c++17)

#
# adjustments that depend on  the availability of external dependencies
#

# if we have mpi
ifeq ($(pyre-gsl.mpi.available), mpi)
# add mpi to the external dependencies
pyre-gsl.ext.extern += mpi
# make sure the {mpi} module has had a chance to export its caspules
pyre-gsl.ext.prerequisites += pyre-mpi.ext
# if not
else
# remove the mpi dependent sources from the build
pyre-gsl.ext.lib.sources.exclude += $(pyre-gsl.ext.lib.prefix)partition.cc
endif

# unconditionally add python to the external libraries
pyre-gsl.ext.extern += python

# if we have numpy
ifeq ($(pyre-gsl.numpy.available), numpy)
# add numpy to the external dependencies
pyre-gsl.ext.extern += numpy
# if not
else
# remove the numpy dependent sources from the build
pyre-gsl.ext.lib.sources.exclude += $(pyre-gsl.ext.lib.prefix)numpy.cc
endif


# get the testsuites
include pyre-gsl.pkg.tests


endif


# end of file
