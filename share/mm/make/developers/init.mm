# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# the name of the developer
developer ?= $(user.username)

# developer choices
developer.$(developer).compilers ?=

# constructor
define developer.init =
    ${foreach
        language,
        $(languages),
        ${foreach
            category,
            $(languages.$(language).categories),
            ${eval developers.$(developer).$(language).$(category) ?=}
        }
    }
endef


# end of file
