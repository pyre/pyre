# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# project global settings
include pyre.def
# my subdirectories
RECURSE_DIRS = \
    lib \
    packages \
    extensions \
    defaults \
    bin \
    templates \
    schema \
    tests \
    examples \
    web \
    bot \
    people

# the pyre install archive
PYRE_ZIP = $(EXPORT_ROOT)/pyre-1.0.zip

# the standard targets
all:
	BLD_ACTION="all" $(MM) recurse

tidy::
	BLD_ACTION="tidy" $(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse

live:
	BLD_ACTION="live" $(MM) recurse

# other targets
build: lib packages extensions defaults bin

test: build tests examples

zip: build zipit

zipit:
	$(RM_F) $(PYRE_ZIP)
	(cd $(EXPORT_ROOT); zip -r ${PYRE_ZIP} * )

# shortcuts for building specific subdirectories
.PHONY: $(RECURSE_DIRS) doc

$(RECURSE_DIRS) doc:
	(cd $@; $(MM))


# end of file
