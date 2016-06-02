# -*- Makefile -*-
#
# authors:
#   Michael Aïvázis <michael.aivazis@para-sim.com>
#   Raúl Radovitzky <raul.radovitzky@para-sim.com>
#
# (c) 2013-2016 all rights reserved
#

# project settings
include {project.name}.def
# my subdirectories
RECURSE_DIRS = \
    graphics \
    scripts \
    styles \

# the exported items
EXPORT_WEB = {project.name}.html

# standard targets
all: export

tidy::
	BLD_ACTION="tidy" $(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse

export:: export-web
	BLD_ACTION="export" $(MM) recurse

live: live-dirs live-web
	BLD_ACTION="live" $(MM) recurse

# end of file
