# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


PROJECT = pyre

#--------------------------------------------------------------------------
#

all: test

test: sanity records sheets csv

sanity:
	${PYTHON} ./sanity.py

records:
	${PYTHON} ./record.py
	${PYTHON} ./record_accessors.py

sheets:
	${PYTHON} ./sheet.py
	${PYTHON} ./sheet_class_layout.py
	${PYTHON} ./sheet_class_inheritance.py
	${PYTHON} ./sheet_class_inheritance_multi.py
	${PYTHON} ./sheet_class_record.py
	${PYTHON} ./sheet_class_inheritance_record.py
	${PYTHON} ./sheet_instance.py

csv:
	${PYTHON} ./csv_instance.py
	${PYTHON} ./csv_read.py


# end of file 
