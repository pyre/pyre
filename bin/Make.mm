# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
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
    listdir.py \
    merlin \
    smith.pyre \
    pyre

export:: export-binaries

release:: release-binaries


# end of file
