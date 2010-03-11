# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


PROJECT = pyre

RECURSE_DIRS = \
    $(PACKAGES)

PACKAGES = \
    pyre

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
#

PYRE_ZIP = $(EXPORT_ROOT)/pyre-${PYRE_VERSION}.zip

zip:
	for package in $(PACKAGES); do { \
	    ( cd $${package}; zip -r ${PYRE_ZIP} $${package}; ) \
	} done


# end of file 
