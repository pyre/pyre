# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


PROJECT = pyre

#--------------------------------------------------------------------------
#

all: test

test: sanity channels

sanity:
	${PYTHON} ./sanity.py

channels:
	${PYTHON} ./debug.py
	${PYTHON} ./debug-activation.py --journal.debug.activation
	${PYTHON} ./debug-activation.py --config=activation.pml
	DEBUG_OPT=activation ${PYTHON} ./debug-activation.py
	${PYTHON} ./debug-injection.py
	${PYTHON} ./firewall.py
	${PYTHON} ./firewall-activation.py --journal.firewall.activation=off
	${PYTHON} ./firewall-activation.py --config=activation.pml
	${PYTHON} ./firewall-injection.py

# end of file 
