# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


PROJECT = pyre
PACKAGE = schema

#--------------------------------------------------------------------------
#

all: tidy

#--------------------------------------------------------------------------
#

EXPORT_ETC = \
    config.html \
    config.xsd \


export:: export-etc


# end of file 
