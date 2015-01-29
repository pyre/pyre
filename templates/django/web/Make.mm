# -*- Makefile -*-
#
# {project.authors}
# {project.affiliations}
# (c) {project.span} all rights reserved
#

# project settings
include {project.name}.def
# the package
PACKAGE=web/www
# the package
EXPORT_WEB = \
    resources \
    templates

# standard targets
all: export

export:: export-web

live: live-web

# end of file
