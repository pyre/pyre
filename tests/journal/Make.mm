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

channels:
	${PYTHON} ./debug.py
	${PYTHON} ./debug-activation.py --journal.debug.activation
	${PYTHON} ./debug-activation.py --config=activation.pml
	DEBUG_OPT=activation ${PYTHON} ./debug-activation.py
	${PYTHON} ./debug-injection.py
	${PYTHON} ./firewall.py

# end of file 
