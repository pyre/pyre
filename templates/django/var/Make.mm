# -*- Makefile -*-
#
# {project.authors}
# {project.affiliations}
# (c) {project.span} all rights reserved
#

# project defaults
include {project.name}.def
# the package name
PACKAGE = var
# the stuff in this directory goes to {{etc/{project.name}/apache}}
EXPORT_ETCDIR = $(EXPORT_ROOT)/$(PACKAGE)/$(PROJECT)

# the standard build targets
all: export

# make sure we scope the files correctly
export:: export-etcdir

# end of file
