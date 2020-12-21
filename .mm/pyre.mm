# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2020 all rights reserved


# pyre builds a python package
pyre.packages := pyre.pkg
# libraries
pyre.libraries := pyre.lib
# the mandatory extensions
pyre.extensions := pyre.ext host.ext
# docker image
pyre.docker-images := pyre.eoan-gcc pyre.eoan-clang pyre.focal-gcc pyre.focal-clang
# and test suites
pyre.tests := pyre.python.tests pyre.pkg.tests pyre.lib.tests pyre.ext.tests sqlite.pkg.tests


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
pyre.lib.extern := journal.lib
pyre.lib.prerequisites += journal.lib
pyre.lib.c++.flags += $($(compiler.c++).std.c++17)


# the pyre extensions
# {libpyre} bindings
pyre.ext.root := extensions/pyre/
pyre.ext.stem := pyre
pyre.ext.pkg := pyre.pkg
pyre.ext.wraps := pyre.lib
pyre.ext.capsule :=
pyre.ext.extern := pyre.lib journal.lib pybind11 python
pyre.ext.lib.c++.flags += $($(compiler.c++).std.c++17)
pyre.ext.lib.prerequisites += journal.lib # pyre.lib is added automatically
# host info
host.ext.root := extensions/host/
host.ext.stem := host
host.ext.pkg := pyre.pkg
host.ext.wraps := pyre.lib
host.ext.capsule :=
host.ext.extern := pyre.lib journal.lib python
host.ext.lib.c++.flags += $($(compiler.c++).std.c++17)
host.ext.lib.prerequisites += journal.lib # pyre.lib is added automatically


# postgres
postgres.ext.root := extensions/postgres/
postgres.ext.stem := postgres
postgres.ext.pkg := pyre.pkg
postgres.ext.wraps := pyre.lib
postgres.ext.capsule :=
postgres.ext.extern := pyre.lib journal.lib libpq python
postgres.ext.lib.c++.flags += $($(compiler.c++).std.c++17)
postgres.ext.lib.prerequisites += journal.lib # pyre.lib is added automatically


# the docker images
pyre.focal-gcc.name := focal-gcc
pyre.focal-clang.name := focal-clang
pyre.eoan-gcc.name := eoan-gcc
pyre.eoan-clang.name := eoan-clang


# get the testsuites
include $(pyre.tests)


# end of file
