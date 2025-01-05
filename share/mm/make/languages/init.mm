# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# the language constructor
#  usage: language.init {language}
define language.init =
    # go through all the registered suffixes and create a map from the suffix to the language
    ${foreach
        extension,
        $(languages.$(1).sources),
        ${eval ext$(extension) := $(1)}
    }
    # assemble the option categories in one pile
    ${eval languages.$(1).categories := \
        $(languages.$(1).categories.compile) $(languages.$(1).categories.link) \
    }
# all done
endef


# end of file
