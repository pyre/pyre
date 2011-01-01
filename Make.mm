# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


PROJECT = pyre

RECURSE_DIRS = \
    lib \
    packages \
    depository \
    tests \
    bin \
    doc \
    schema \
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


PYRE_ZIP = $(EXPORT_ROOT)/pyre-${PYRE_VERSION}.zip

zip: tidy
	zip -r ${PYRE_ZIP} packages depository -x \*Make.mm 


# end of file 
