# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# the list of all extensions encountered
extensions ?=

# the extension constructor
#   usage: extensions.init {project} {extension}
define extensions.init =
    # add it to the pile
    ${eval extensions += $(2)}
    # save the project
    ${eval $(2).project := $(1)}
    # set the home
    ${eval $(2).home ?= $($(1).home)/}
    # connect to my package
    ${eval $(2).pkg ?= $($(2).project).pkg}
    # and the (optional) library whose python bindings these are
    ${eval $(2).wraps ?=}

    # the stem for generating extension specific names; it gets used to build the extension
    # archive name, the include directory with the public headers, and the name of the module
    # shared object
    ${eval $(2).stem ?= $($(1).stem)}
    # form the name
    ${eval $(2).name ?= ext$($(2).stem)}

    # the list of external dependencies
    ${eval $(2).extern ?=}
    # initialize the list of requested project dependencies
    ${eval $(2).extern.requested ?= $($(2).extern)}
    # the list of external dependencies that we have support for
    ${eval $(2).extern.supported ?= ${call extern.is.supported,$($(2).extern.requested)}}
    # the list of dependencies in the order they affect the compiler command lines
    ${eval $(2).extern.available ?= ${call extern.is.available,$($(2).extern.supported)}}

    # a list of additional prerequisites for the top target
    ${eval $(2).prerequisites ?=}

    # layout
    # the root of the extension source tree relative to the project home
    ${eval $(2).root ?= ext/$($(2).stem)/}
    # the absolute path to the extension source tree
    ${eval $(2).prefix ?= $($($(2).project).home)/$($(2).root)}
    # a temporary area
    ${eval $(2).tmpdir ?= $($(1).tmpdir)$($(2).name)/}

    # the name of the main module file
    ${eval $(2).module ?= $($(2).stem)}
    # the translation unit with the python initialization file
    ${eval $(2).module.main ?= ${call extension.module.main,$(2)}}
    # the source file with the python initialization routine
    ${eval $(2).module.init ?= ${call extension.module.init,$(2)}}
    # the language of the initialization routine determines the compiler to use
    ${eval $(2).module.language ?= $(ext${suffix $($(2).module.init)})}
    # the name of the shared object
    ${eval $(2).module.so ?= ${call extension.module.dll,$(2)}}

    # extensions may share their capsules
    ${eval $(2).capsule ?= capsules.h}
    # and publish them here, relative to (builder.dest.inc)
    ${eval $(2).capsule.destination ?=}

    # the name of the support archive
    ${eval $(2).lib ?= $(2).lib}
    # its stem
    ${eval $(2).lib.stem ?= $($(2).stem)module}
    # its location
    ${eval $(2).lib.root ?= $($(2).root)}
    # its external dependencies
    ${eval $(2).lib.extern ?= $($(2).extern)}
    # add the library it wraps to its prerequisites
    ${eval $(2).lib.prerequisites += $($(2).wraps)}
    # in general, extensions have no public headers
    ${eval $(2).lib.headers ?=}
    # construct it
    ${call libraries.init,$(1),$(2).lib}
    # adjust its sources
    ${eval $(2).lib.sources := ${call extension.sources,$(2),$(2).lib}}
    # suppress the creation of the support dll
    ${eval $(2).lib.dll :=}

endef


# helpers

# identify the extension main file
#   usage: extension.module.main {extension}
define extension.module.main
    ${strip
        ${foreach suffix,$(languages.sources),
            ${wildcard $($(1).prefix)$($(1).module)$(suffix)}
            ${wildcard $($(1).prefix)__init__$(suffix)}
        }
    }
endef


# identify the extension init file
#   usage: extension.module.init {extension}
define extension.module.init =
    ${strip
	${if ${filter $(languages.cython.sources),${suffix $($(1).module.main)}},
            ${addprefix $($(1).tmpdir),
                ${notdir $($(1).module.main:$(languages.cython.sources)=.cc)}
            },
            $($(1).module.main)
        }
    }
endef


# build the path to where the module dll gets deposited
#   usage: extension.module.dll {extension}
define extension.module.dll
    $($($(1).pkg).pycdir)$($($(1).pkg).ext)$($(1).stem)$($(compiler.python).suffix.module)
endef


# collect the set of sources that comprise the extension supporting library
#   usage: extension.sources {extension} {library}
define extension.sources
    ${strip
        ${filter-out $($(1).module.init),$($(2).sources)}
    }
endef


# end of file
