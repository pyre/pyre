# -*- Makefile -*-
#
# {project.authors}
# {project.affiliations}
# (c) {project.span} all rights reserved
#

# project defaults
include {project.name}.def
# the package name
PACKAGE = {project.name}/actions

# the configuration files
EXPORT_ETC = \
    debug.py

# add these to the clean pile
PROJ_CLEAN = $(EXPORT_ETCDIR)/$(PACKAGE)


# the standard build targets
all: export

export:: export-package-etc

# end of file
