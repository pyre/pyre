# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


PROJECT = pyre

RECURSE_DIRS = \
    lib \
    packages \
    extensions \
    depository \
    bin \
    schema \
    tests \
    examples \

#--------------------------------------------------------------------------
#

all:
	BLD_ACTION="all" $(MM) recurse

tidy::
	BLD_ACTION="tidy" $(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse


#--------------------------------------------------------------------------
#  shortcuts to building in my subdirectories
.PHONY: doc lib extensions packages tests

doc:
	(cd doc; $(MM))

lib:
	(cd lib; $(MM))

depository:
	(cd depository; $(MM))

extensions:
	(cd extensions; $(MM))

packages:
	(cd packages; $(MM))

tests:
	(cd tests; $(MM))

build: lib extensions packages depository


PYRE_ZIP = $(EXPORT_ROOT)/pyre-1.0.zip
zip: packages depository
	(cd $(EXPORT_ROOT); zip -r ${PYRE_ZIP} * -x \*Make.mm )


# end of file 
