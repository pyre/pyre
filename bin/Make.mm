# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#

# project defaults
include pyre.def
# the package name
PACKAGE = bin
# the files
EXPORT_BINS = \
    class.pyre \
    listdir.py \
    merlin \
    smith.pyre \
    pyre

# add these to the clean pile
PROJ_CLEAN = ${{addprefix $(EXPORT_BINDIR)/, $(EXPORT_BINS)}}

# the standard targets
all: export

export:: export-binaries

live: live-bin

# end of file
