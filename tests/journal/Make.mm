# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


PROJECT = pyre

#--------------------------------------------------------------------------
#

working: debug

all: test

test: sanity journal debug

sanity:
	${PYTHON} ./sanity.py

journal:
	${PYTHON} ./journal_cmdline.py --journal.debug.pyre.test1 --journal.debug.pyre.test2=off

debug:
	${PYTHON} ./debug.py

# end of file 
