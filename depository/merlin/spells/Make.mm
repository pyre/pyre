# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


PROJECT = pyre
PACKAGE = depository/merlin/spells

#--------------------------------------------------------------------------
#

all: export


#--------------------------------------------------------------------------
#

EXPORT_ETCDIR = $(EXPORT_ROOT)
EXPORT_ETC = \
   builtin.py \

export:: export-etc


# end of file 
