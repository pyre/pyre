# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# language specific settings
# initialize the platform specific flags for each language option category
${foreach \
    language, \
    $(languages), \
    ${foreach \
        category, \
        $(languages.$(language).categories), \
        ${eval platform.$(language).$(category) ?=} \
    } \
}

# build the environment variable
platform.macro := MM_PLATFORM_${subst -,_,$(platform)}

# fine adjustments
platform.c.defines := $(platform.macro)
platform.c++.defines := $(platform.macro)
platform.cuda.defines := $(platform.macro)
platform.fortran.defines := $(platform.macro)


# end of file
