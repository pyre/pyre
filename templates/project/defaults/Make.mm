# -*- Makefile -*-
#
# {project.authors}
# {project.affiliations}
# (c) {project.span} all rights reserved
#

# project defaults
include {project.name}.def
# the package name
PACKAGE = defaults

# the configuration files
EXPORT_ETC = \
    {project.name}.cfg

# the standard build targets
all: export

export:: export-etc

# end of file
