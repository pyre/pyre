# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved

# establish the build order; {merlin} leads so it stages the {lib/mm} portinfo headers
# into {include/mm} before any project with C++ sources compiles against them
projects := merlin pyre journal pyre-mpi pyre-gsl pyre-cuda survey

# end of file
