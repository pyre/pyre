# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


PROJECT = pyre
PACKAGE = schema

#--------------------------------------------------------------------------
#

all: tidy

#--------------------------------------------------------------------------
#

EXPORT_ETCDIR = $(EXPORT_ROOT)
EXPORT_ETC = \
    inventory.html \
    inventory.xsd \


export:: export-etc


# end of file 
