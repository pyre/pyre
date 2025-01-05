# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# the builder constructor
#   usage: builder.init {project-prefix} {project-bldroot}
define builder.init =
    # the build tag
    ${eval builder.tid ?= $(target.tag)}

    # construct the name of the top level directory
    ${eval builder.dest.prefix ?= $(1)/}

    # the layout of the products directory
    ${eval builder.dest.bin ?= $(builder.dest.prefix)bin/}
    ${eval builder.dest.share ?= $(builder.dest.prefix)share/}
    ${eval builder.dest.doc ?= $(builder.dest.prefix)doc/}
    ${eval builder.dest.etc ?= $(builder.dest.prefix)etc/}
    ${eval builder.dest.inc ?= $(builder.dest.prefix)include/}
    ${eval builder.dest.lib ?= $(builder.dest.prefix)lib/}
    ${eval builder.dest.pyc ?= $(builder.dest.prefix)packages/}

    # the layout of the staging area with the build disposables
    ${eval builder.staging ?= $(2)/$(builder.tid)/}

    # make a pile out for all the relevant directories; this gets used by the rule maker that makes
    # sure these directories exist, so make sure you add new ones here as well
    ${eval builder.dirs := prefix bin doc inc lib pyc share}
    # put them all on a pile
    ${eval builder.directories := \
        ${sort \
            ${foreach directory,$(builder.dirs),$(builder.dest.$(directory))} \
        } \
        $(builder.staging)
    }

    # extensions for products
    builder.ext.obj := .o
    builder.ext.dep := .d
    builder.ext.lib := .a
    builder.ext.dll := .so

# all done
endef


# end of file
