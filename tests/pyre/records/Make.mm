# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#
#


PROJECT = pyre

#--------------------------------------------------------------------------
#

all: test

test: sanity records dynamicrecords csv

sanity:
	${PYTHON} ./sanity.py

records:
	${PYTHON} ./record.py
	${PYTHON} ./record_layout.py
	${PYTHON} ./record_inheritance.py
	${PYTHON} ./record_inheritance_multi.py
	${PYTHON} ./record_raw.py
	${PYTHON} ./record_kwds.py
	${PYTHON} ./record_conversions.py
	${PYTHON} ./record_validations.py
	${PYTHON} ./record_derivations.py
	${PYTHON} ./record_derivations_inheritance.py

dynamicrecords:
	${PYTHON} ./dynamicrecord.py
	${PYTHON} ./dynamicrecord_layout.py
	${PYTHON} ./dynamicrecord_inheritance.py
	${PYTHON} ./dynamicrecord_inheritance_multi.py
	${PYTHON} ./dynamicrecord_derivations.py
	${PYTHON} ./dynamicrecord_derivations_inheritance.py

csv:
	${PYTHON} ./csv_instance.py
	${PYTHON} ./csv_read.py
	${PYTHON} ./csv_read_partial.py
	${PYTHON} ./csv_read_derivations.py
	${PYTHON} ./csv_bad_source.py


# end of file 
