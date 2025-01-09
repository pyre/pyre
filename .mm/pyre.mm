# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# pyre builds a python package
pyre.packages := pyre.pkg
# libraries
pyre.libraries := pyre.lib
# the mandatory extensions
pyre.extensions := pyre.ext host.ext
# docker image
pyre.docker-images := \
    pyre.focal-gcc pyre.focal-clang \
    pyre.groovy-gcc pyre.groovy-clang pyre.groovy-cuda \
    pyre.hirsute-gcc pyre.hirsute-clang pyre.hirsute-gcc-cmake \
    pyre.impish-gcc pyre.impish-clang \
    pyre.jammy-gcc pyre.jammy-clang

# and test suites
pyre.tests := pyre.python.tests pyre.pkg.tests pyre.lib.tests pyre.ext.tests sqlite.pkg.tests

# we also some files that get moved verbatim
pyre.verbatim := pyre.templates


# predicates that check the c++ standard in use
# these are low resolution tests and may not be good enough
pyre.c++20 = \
  ${findstring \
    $($(compiler.c++).std.c++20), \
    $(pyre.lib.c++.flags) \
  }


# if we have {hdf5}, build the {h5} extension
${if ${findstring hdf5,$(extern.available)},\
    ${eval pyre.extensions += h5.ext} \
}


# if we have {libpq}, build the {postgres} extension and test it
${if ${findstring libpq,$(extern.available)},\
    ${eval pyre.extensions += postgres.ext} \
    ${eval pyre.tests += postgres.ext.tests} \
}


# the pyre package meta-data
pyre.pkg.root := packages/pyre/
pyre.pkg.stem := pyre
pyre.pkg.drivers := pyre pyre-config smith.pyre
pyre.pkg.config := pyre
pyre.pkg.ext := extensions/


# the pyre library meta-data
pyre.lib.root := lib/pyre/
pyre.lib.stem := pyre
pyre.lib.prerequisites += journal.lib
pyre.lib.c++.defines += PYRE_CORE
pyre.lib.c++.flags += -Wall $($(compiler.c++).std.c++17)

# additional macros that enable features sensitive to the c++ standard version
pyre.lib.c++.defines += \
  ${if $(pyre.c++20),\
    HAVE_COMPACT_PACKINGS WITH_CXX20 \
  }

# external dependencies
pyre.lib.extern := \
    journal.lib \
    ${if ${findstring hdf5,$(extern.available)}, \
        hdf5 \
        ${if ${findstring mpi,$(hdf5.parallel)},mpi} \
    } \


# the pyre extensions
# {libpyre} bindings
pyre.ext.root := extensions/pyre/
pyre.ext.stem := pyre
pyre.ext.pkg := pyre.pkg
pyre.ext.wraps := pyre.lib
pyre.ext.capsule :=
pyre.ext.extern := journal.lib pybind11 python
pyre.ext.lib.c++.flags += $(pyre.lib.c++.flags)
pyre.ext.lib.c++.defines += $(pyre.lib.c++.defines)
pyre.ext.lib.prerequisites += journal.lib # pyre.lib is added automatically
# host info
host.ext.root := extensions/host/
host.ext.stem := host
host.ext.pkg := pyre.pkg
host.ext.wraps := pyre.lib
host.ext.capsule :=
host.ext.extern := journal.lib python
host.ext.lib.c++.flags += $(pyre.lib.c++.flags)
host.ext.lib.c++.defines += $(pyre.lib.c++.defines)
host.ext.lib.prerequisites += journal.lib # pyre.lib is added automatically


# hdf5
h5.ext.root := extensions/h5/
h5.ext.stem := h5
h5.ext.pkg := pyre.pkg
h5.ext.wraps := pyre.lib
h5.ext.capsule :=
h5.ext.extern = journal.lib hdf5 ${if ${findstring mpi,$(hdf5.parallel)},mpi} pybind11 python
h5.ext.lib.c++.flags += $(pyre.lib.c++.flags)
h5.ext.lib.c++.defines += $(pyre.lib.c++.defines)
h5.ext.lib.prerequisites += journal.lib # pyre.lib is added automatically


# postgres
postgres.ext.root := extensions/postgres/
postgres.ext.stem := postgres
postgres.ext.pkg := pyre.pkg
postgres.ext.wraps := pyre.lib
postgres.ext.capsule :=
postgres.ext.extern := journal.lib libpq python
postgres.ext.lib.c++.flags += $(pyre.lib.c++.flags)
postgres.ext.lib.c++.defines += $(pyre.lib.c++.defines)
postgres.ext.lib.prerequisites += journal.lib # pyre.lib is added automatically


# the docker images
# focal
pyre.focal-gcc.name := focal-gcc
pyre.focal-clang.name := focal-clang
# groovy
pyre.groovy-gcc.name := groovy-gcc
pyre.groovy-clang.name := groovy-clang
pyre.groovy-cuda.name := groovy-cuda
pyre.groovy-cuda.launch.mounts := mm pyre
# hirsute
pyre.hirsute-gcc.name := hirsute-gcc
pyre.hirsute-clang.name := hirsute-clang
pyre.hirsute-gcc-cmake.name := hirsute-gcc-cmake
# impish
pyre.impish-gcc.name := impish-gcc
pyre.impish-clang.name := impish-clang
# jammy
pyre.jammy-gcc.name := jammy-gcc
pyre.jammy-clang.name := jammy-clang

# the templates
pyre.templates.root := templates/


# get the test suites
include $(pyre.tests)


# end of file
