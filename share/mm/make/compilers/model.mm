# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# assemble the list of compilers
#    order: defaults from the platform, then user configuration files, then mm command line
compilers := \
    $(platform.compilers) $(target.compilers) \
    $(developer.$(developer).compilers) \
    $(mm.compilers)

# include the compiler specific configuration files
include $(compilers:%=make/compilers/%.mm)

# language specific settings
# initialize the compiler specific flags for each language option category
${foreach \
    language, \
    $(languages), \
    ${if ${value compiler.$(language)}, \
        ${foreach \
            category, \
            $(languages.$(language).categories), \
            ${eval $(compiler.$(language)).$(category) ?=} \
        } \
    } \
}


# end of file
