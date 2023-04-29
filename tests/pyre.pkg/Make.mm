# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2023 all rights reserved
#


PROJECT = pyre

RECURSE_DIRS = \
    primitives \
    patterns \
    grid \
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
    flow \
    pyre


# the support in {pyre.external} is still very experimental and the test cases are still in debugging mode
# now that journal errors are fatal, these tests stop the buld
# skip until the support improves a bit
SKIP = \
    externals \

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

# shortcuts for building specific subdirectories
.PHONY: $(RECURSE_DIRS)

$(RECURSE_DIRS):
	(cd $@; $(MM))

# end of file
