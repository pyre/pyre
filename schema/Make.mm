# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
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
