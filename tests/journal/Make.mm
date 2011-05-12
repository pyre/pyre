# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


PROJECT = pyre

#--------------------------------------------------------------------------
#

working: channels

all: test

test: sanity journal channels

sanity:
	${PYTHON} ./sanity.py

journal:
	${PYTHON} ./journal_cmdline.py --journal.debug.pyre.test1 --journal.debug.pyre.test2=off

channels:
	${PYTHON} ./debug.py
	${PYTHON} ./debug-injection.py
	${PYTHON} ./firewall.py

# end of file 
