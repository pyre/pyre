# -*- Makefile -*-
#
# {project.authors}
# {project.affiliations}
# (c) {project.span} all rights reserved
#

# access the project defaults
include {project.name}.def
# the package name
PACKAGE = {project.name}
# clean up
PROJ_CLEAN += $(EXPORT_MODULEDIR)

# the list of directories to visit
RECURSE_DIRS = \
    actions \
    components \
    extensions \

# the list of python modules
EXPORT_PYTHON_MODULES = \
    __init__.py

# grab the revision number
REVISION = ${{strip ${{shell bzr revno}}}}
# if not there
ifeq ($(REVISION),)
REVISION = 0
endif

# the standard build targets
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

# construct my {{__init__.py}}
__init__.py: __init__py
	@sed -e "s:REVISION:$(REVISION):g" __init__py > __init__.py


# end of file
