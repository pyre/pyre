# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# chroma builds a header-only c++ library that is the single source of color truth
chroma.libraries := chroma.lib
# it ships no python package
chroma.packages :=
# and no extension of its own; its bindings ride along with {libpyre}
chroma.extensions :=
# but it does carry a test suite
chroma.tests := chroma.lib.tests


# the chroma library meta-data
chroma.lib.stem := chroma
# the source lives in a top-level directory so the library sits below {journal} and {pyre}
chroma.lib.root := lib/chroma/
# deposit the headers under the {pyre} namespace so they never collide in a shared prefix
chroma.lib.incdir := $(builder.dest.inc)pyre/chroma/
# the gateway header is deposited one level above the rest, as {pyre/chroma.h}
chroma.lib.gateway := chroma.h


# get the test suites
include $(chroma.tests)


# end of file
