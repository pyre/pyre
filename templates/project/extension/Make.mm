# -*- Makefile -*-
#
# {project.authors}
# {project.affiliations}
# (c) {project.span}  all rights reserved
#

# get the global defaults for the {{{project.name}}} project
include {project.name}.def
# the local package
PACKAGE = extensions
MODULE = {project.name}

# support for making python extensions
include std-pythonmodule.def

# adjust the build parameters
PROJ_TMPDIR = $(BLD_TMPDIR)/$(PROJECT)/$(PACKAGE)
PROJ_LCXX_LIBPATH=$(BLD_LIBDIR)

# the list of extension source files
PROJ_SRCS = \
    exceptions.cc \
    metadata.cc

# my dependencies
PROJ_LIBRARIES += -l{project.name} -ljournal

# register the dependence on {{lib{project.name}}} so I get recompiled when it changes
PROJ_OTHER_DEPENDENCIES = $(BLD_LIBDIR)/lib{project.name}.$(EXT_AR)

# end of file
