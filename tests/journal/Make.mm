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
	${PYTHON} ./info.py
	${PYTHON} ./info-activation.py --journal.info.activation
	${PYTHON} ./info-activation.py --config=activation.pml
	${PYTHON} ./info-injection.py
	${PYTHON} ./warning.py
	${PYTHON} ./warning-activation.py --journal.warning.activation=off
	${PYTHON} ./warning-activation.py --config=activation.pml
	${PYTHON} ./warning-injection.py
	${PYTHON} ./error.py
	${PYTHON} ./error-activation.py --journal.error.activation=off
	${PYTHON} ./error-activation.py --config=activation.pml
	${PYTHON} ./error-injection.py

# end of file 
