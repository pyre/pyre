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

# add these to the clean pile
PROJ_CLEAN = ${{addprefix $(EXPORT_ETCDIR)/, $(EXPORT_ETC)}}


# the standard build targets
all: export

export:: export-etc

# end of file
