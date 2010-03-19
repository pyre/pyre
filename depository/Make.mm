# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


PROJECT = pyre
PACKAGE = depository

#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
#

EXPORT_ETCDIR = $(EXPORT_ROOT)
EXPORT_ETC = \
    pyre.pcs

export:: export-etc


# end of file 
