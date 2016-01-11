# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# project defaults
include merlin.def
# package name
PACKAGE = merlin
# my subfolders
RECURSE_DIRS = \
    assets \
    components \
    schema \
    spells \
# the python modules
EXPORT_PYTHON_MODULES = \
    __init__.py

# standard targets
all: export

tidy::
	BLD_ACTION="tidy" $(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse

export:: __init__.py export-python-modules
	BLD_ACTION="export" $(MM) recurse
	@$(RM) __init__.py

live: live-python-modules
	BLD_ACTION="live" $(MM) recurse

# construct my {__init__.py}
__init__.py: __init__py Make.mm
	@sed \
          -e "s:MERLIN_MAJOR:$(PROJECT_MAJOR):g" \
          -e "s:MERLIN_MINOR:$(PROJECT_MINOR):g" \
          -e "s:BZR_REVNO:$$(bzr revno):g" \
          -e "s|DATE_COMPILED|$$(date -u)|g" \
          __init__py > __init__.py

# end of file
