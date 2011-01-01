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

test: sanity constraints

sanity:
	${PYTHON} ./sanity.py
	${PYTHON} ./exceptions.py

constraints:
	${PYTHON} ./isAll.py
	${PYTHON} ./isAny.py
	${PYTHON} ./isBetween.py
	${PYTHON} ./isEqual.py
	${PYTHON} ./isGreater.py
	${PYTHON} ./isGreaterEqual.py
	${PYTHON} ./isLess.py
	${PYTHON} ./isLessEqual.py
	${PYTHON} ./isLike.py
	${PYTHON} ./isMember.py
	${PYTHON} ./isNegative.py
	${PYTHON} ./isNot.py
	${PYTHON} ./isPositive.py
	${PYTHON} ./isSubset.py
	${PYTHON} ./and.py
	${PYTHON} ./or.py


# end of file 
