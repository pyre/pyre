# -*- Makefile -*-
#
# {project.authors}
# {project.affiliations}
# (c) {project.span} all rights reserved
#

# project settings
include {project.name}.def

EXPORT_WEB = \
    resources \
    templates

# standard targets
all: export

export:: export-web

# end of file
