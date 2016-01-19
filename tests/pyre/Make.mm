# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


PROJECT = pyre

RECURSE_DIRS = \
    primitives \
    patterns \
    parsing \
    units \
    filesystem \
    xml \
    schemata \
    constraints \
    algebraic \
    calc \
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
    nexus \
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
