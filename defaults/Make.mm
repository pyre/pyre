# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


PROJECT = pyre
PACKAGE = defaults

RECURSE_DIRS = \
    merlin \
    pyre \

#--------------------------------------------------------------------------
#

all: export


tidy::
	BLD_ACTION="tidy" $(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse


#--------------------------------------------------------------------------
#

EXPORT_ETC = \
    merlin.cfg \
    pyre.cfg


export:: export-etc
	BLD_ACTION="export" $(MM) recurse

release:: release-etc
	BLD_ACTION="release" $(MM) recurse


# end of file
