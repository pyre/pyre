# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# project defaults
include pyre.def


all: test

test: sanity nodes clean

sanity:
	${PYTHON} ./sanity.py
	${PYTHON} ./node.py

nodes:
	${PYTHON} ./node_instantiation.py
	${PYTHON} ./node_signals.py


# end of file
