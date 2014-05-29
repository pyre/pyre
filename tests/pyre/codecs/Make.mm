# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#
#


PROJECT = pyre

#--------------------------------------------------------------------------
#

all: test

test: sanity formats

sanity:
	${PYTHON} ./sanity.py
	${PYTHON} ./exceptions.py
	${PYTHON} ./manager.py

formats: pml cfg

pml:
	${PYTHON} ./pml.py
	${PYTHON} ./pml_empty.py
	${PYTHON} ./pml_badRoot.py
	${PYTHON} ./pml_unknownNode.py
	${PYTHON} ./pml_badNode.py
	${PYTHON} ./pml_badAttribute.py
	${PYTHON} ./pml_package.py
	${PYTHON} ./pml_packageNested.py
	${PYTHON} ./pml_componentFamily.py
	${PYTHON} ./pml_componentName.py
	${PYTHON} ./pml_componentConditional.py
	${PYTHON} ./pml_componentConditionalNested.py
	${PYTHON} ./pml_sample.py

cfg:
	${PYTHON} ./cfg.py
	${PYTHON} ./cfg_empty.py
	${PYTHON} ./cfg_badToken.py
	${PYTHON} ./cfg_marker.py
	${PYTHON} ./cfg_open.py
	${PYTHON} ./cfg_close.py


# end of file 
