# -*- Makefile -*-
# -*- coding: utf-8 -*-
#
# {pyre.user.name}
# {pyre.user.affiliation}
# (c) {project.span} all rights reserved
#

# access the project defaults
include {project.name}.def

# adjust the build parameters
PROJ_LIB = $(PROJ_LIBDIR)/lib{project.name}.$(EXT_LIB)

# the list of sources to compile
PROJ_SRCS = \
    version.cc

# the public headers
EXPORT_HEADERS = \
    version.h

# the library
EXPORT_LIBS = $(PROJ_LIB)

# the default target compiles this library and exports it
all: export-headers proj-lib export-libraries


# end of file 
