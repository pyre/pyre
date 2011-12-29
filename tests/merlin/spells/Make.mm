# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


PROJECT = pyre

PROJ_CLEAN += \
    .merlin \
    deep \
    shallow \

MERLIN = ${EXPORT_BINDIR}/merlin

#--------------------------------------------------------------------------
#

all: test

test: init clean

init:
	${MERLIN} init shallow
	${MERLIN} init --create-prefix deep/ly/burried

# end of file 
