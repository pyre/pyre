# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#

# access the project defaults
include pyre.def
# the package name
PACKAGE = nexus
# my folders
RECURSE_DIRS = \
    http \
# python packages
EXPORT_PYTHON_MODULES = \
    Nexus.py \
    Node.py \
    Server.py \
    Service.py \
    exceptions.py \
    services.py \
    __init__.py

# the standard build targets
all: export

tidy::
	BLD_ACTION="tidy" $(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse

export:: export-package-python-modules
	BLD_ACTION="export" $(MM) recurse

live: live-package-python-modules
	BLD_ACTION="live" $(MM) recurse

#  shortcuts for building specific subdirectories
.PHONY: $(RECURSE_DIRS)

$(RECURSE_DIRS):
	(cd $@; $(MM))

# end of file
