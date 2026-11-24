# -*- makefile -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# check availability: the library talks to the server through the interfaces libpq 17 introduced,
# and an older libpq leaves it out of the build
libpq.available := ${call extern.is.atLeast,libpq,17}

# if a recent enough {libpq} is available
ifeq ($(libpq.available), libpq)


# postgres ships no python package of its own; its python lives in {packages/pyre/db}, part of
# {pyre.pkg}
pyre-postgres.packages :=
# a library
pyre-postgres.libraries := pyre-postgres.lib
# a python extension, deposited into the {pyre} package that hosts it
pyre-postgres.extensions := pyre-postgres.ext
# the library stands on its own, so it gets a c++ suite of its own; the extension suite exercises
# the bindings, and the package suite exercises {pyre.db} against the server. all three are
# skipped whole when no server answers
pyre-postgres.tests := pyre-postgres.lib.tests pyre-postgres.ext.tests pyre-postgres.pkg.tests


# the postgres library meta-data; it is header only, and it knows nothing about python
pyre-postgres.lib.root := lib/postgres/
pyre-postgres.lib.stem := pyre-postgres
# deposit the headers under the {pyre} namespace so they never collide in a shared prefix
pyre-postgres.lib.incdir := $(builder.dest.inc)pyre/postgres/
# the gateway header is deposited one level above the rest, as {pyre/postgres.h}
pyre-postgres.lib.gateway := postgres.h
pyre-postgres.lib.prerequisites := journal.lib
pyre-postgres.lib.extern := journal.lib libpq
pyre-postgres.lib.c++.flags += $(pyre.lib.c++.flags)
pyre-postgres.lib.c++.defines += $(pyre.lib.c++.defines)

# the postgres extension meta-data; it wraps the library above
pyre-postgres.ext.root := extensions/postgres/
# the module stays {postgres}; {packages/pyre/extensions} re-exports it as {libpq}
pyre-postgres.ext.stem := postgres
# the module rides in the {pyre} package, alongside {libpyre}
pyre-postgres.ext.pkg := pyre.pkg
pyre-postgres.ext.wraps := pyre-postgres.lib
pyre-postgres.ext.capsule :=
pyre-postgres.ext.extern := pyre.lib journal.lib libpq pybind11 python
pyre-postgres.ext.lib.c++.flags += $(pyre-postgres.lib.c++.flags)
pyre-postgres.ext.lib.c++.defines += $(pyre-postgres.lib.c++.defines)
pyre-postgres.ext.lib.prerequisites += pyre-postgres.lib journal.lib # pyre.lib is added automatically


# get the testsuites
# is a live postgres server reachable? probe only if {pg_isready} exists, so no server (or no tool)
# is quiet; the suites below exclude all their drivers when this is empty
postgres.live := ${shell command -v pg_isready > /dev/null 2>&1 && pg_isready -q && echo live}

include pyre-postgres.lib.tests pyre-postgres.ext.tests pyre-postgres.pkg.tests


endif


# end of file
