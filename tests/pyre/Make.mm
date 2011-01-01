# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


PROJECT = pyre

RECURSE_DIRS = \
    patterns \
    tracking \
    parsing \
    xml \
    units \
    schema \
    constraints \
    calc \
    records \
    tabular \
    filesystem \
    codecs \
    config \
    framework \
    components \

#--------------------------------------------------------------------------
#

all: test

test::
	BLD_ACTION="test" $(MM) recurse

tidy::
	BLD_ACTION="tidy" $(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse


# end of file 
