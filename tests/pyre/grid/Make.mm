# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2017 all rights reserved
#


# project defaults
include pyre.def


all: test

test: sanity tile

sanity:
	${PYTHON} ./sanity.py

tile:
	${PYTHON} ./tile.py


# end of file
