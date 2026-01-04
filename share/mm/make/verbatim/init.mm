# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the list of verbatim assets encountered
verbatim ?=

# the verbatim asset constructor
define verbatim.init =
    # add this to the pile
    ${eval verbatim += $(2)}
    # save the project
    ${eval $(2).project := $(1)}

    # set the home
    ${eval $(2).home ?= $($(1).home)/}
    # the path to the assets relative to the project home
    ${eval $(2).root ?=}
    # build the absolute path to the verbatim asset directory
    ${eval $(2).prefix ?= $($(2).home)$($(2).root)}
    # and the destination directory
    ${eval $(2).staging ?= $(builder.dest.prefix)$($(2).root)}

    # compute the set of files
    # at the source
    ${eval $(2).assets ?= ${call verbatim.assets,$(2)}}
    ${eval $(2).directories ?= ${call verbatim.directories,$(2)}}

    # at the destination
    ${eval $(2).staging.assets := ${call verbatim.staging.assets,$(2)}}
    ${eval $(2).staging.directories := ${call verbatim.staging.directories,$(2)}}

    # cruft that must be here to silence undefined variable warnings
    # the list of external dependencies as requested by the user
    ${eval $(2).extern :=}
    # initialize the list of requested project dependencies
    ${eval $(2).extern.requested :=}
    # the list of external dependencies that we have support for
    ${eval $(2).extern.supported :=}
    # the list of dependencies in the order they affect the compiler command lines
    ${eval $(2).extern.available :=}

endef


# build the set of verbatim files
#  usage verbatim.assets {package}
define verbatim.assets =
    ${realpath
        ${shell find $($(1).prefix) -type f}
    }
endef


# build the set of verbatim directories
#  usage verbatim.directories {package}
# N.B.: the /* removes the root directory from the pile and prevents the creation of a duplicate
#       target; an alternative would have been to sort/uniq the pile, but why...
define verbatim.directories =
    ${addsuffix /,
        ${realpath
            ${shell find $($(1).prefix)/* -type d}
        }
    }
endef


# build the set of staged verbatim files
#  usage verbatim.staging.assets {package}
define verbatim.staging.assets =
    ${subst $($(1).prefix),$($(1).staging),$($(1).assets)}
endef


# build the set of staged verbatim
#  usage verbatim.staging.directories {package}
define verbatim.staging.directories =
    ${subst $($(1).prefix),$($(1).staging),$($(1).directories)}

endef


# end of file
