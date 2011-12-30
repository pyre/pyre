# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


PROJECT = gauss.pyre
PACKAGE = depository

#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
#

EXPORT_ETCDIR = $(EXPORT_ROOT)
EXPORT_ETC = \
    gauss.pml


export:: export-etc


# end of file 
