# -*- Makefile -*-
#
# {project.authors}
# {project.affiliations}
# (c) {project.span} all rights reserved
#

# project defaults
include {project.name}.def
# the package name
PACKAGE = bin
# the list of files
EXPORT_BINS = \
    {project.name}

# the standard build targets
all: export

export:: export-binaries

# end of file
