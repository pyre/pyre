# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


PROJECT = pyre

RECURSE_DIRS = \
    patterns \
    parsing \
    units \
    filesystem \
    xml \
    constraints \
    algebraic \
    calc \
    schemata \
    descriptors \
    records \
    tabular \
    tracking \
    codecs \
    config \
    framework \
    components \
    timers \
    weaver \
    db \
    ipc \
    platforms \
    shells \
    externals \
    pyre

#--------------------------------------------------------------------------
#

all: 
	BLD_ACTION="all" $(MM) recurse

test::
	BLD_ACTION="test" $(MM) recurse

tidy::
	BLD_ACTION="tidy" $(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse


# end of file 
