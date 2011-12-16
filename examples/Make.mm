# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#
#


PROJECT = pyre

RECURSE_DIRS = \
    gauss.pyre

# add these if the corresponding support has been built
# postgres
LIBPQ_DIR= # overriden by the the environment
ifneq ($(strip $(LIBPQ_DIR)),)

  RECURSE_DIRS += \
      bizbook.pyre \
      contacts.pyre

endif

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


# end of file 
