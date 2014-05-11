# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


PROJECT = pyre
PACKAGE = bin

#--------------------------------------------------------------------------
#

all: export


#--------------------------------------------------------------------------
# export

EXPORT_BINS = \
    class.pyre \
    merlin \
    project.pyre \
    pyre

export:: export-binaries

release:: release-binaries


# end of file 
