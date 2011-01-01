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

test: sanity records sheets csv views charts pivots

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
	${PYTHON} ./sheet_populate.py
	${PYTHON} ./sheet_columns.py
	${PYTHON} ./sheet_index.py
	${PYTHON} ./sheet_updates.py

views:
	${PYTHON} ./view.py

charts:
	${PYTHON} ./chart.py
	${PYTHON} ./chart_class_layout.py
	${PYTHON} ./chart_class_inheritance.py
	${PYTHON} ./chart_instance.py
	${PYTHON} ./chart_inferred.py
	${PYTHON} ./chart_interval.py
	${PYTHON} ./chart_instance_config.py
	${PYTHON} ./chart_filter.py
	${PYTHON} ./chart_sales.py

pivots:
	${PYTHON} ./pivot.py

csv:
	${PYTHON} ./csv_instance.py
	${PYTHON} ./csv_read.py


# end of file 
