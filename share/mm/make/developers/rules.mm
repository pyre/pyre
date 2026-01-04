# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# developer info
developer.info:
	@${call log.sec,"developer", "options and overrides from '$(developer)'"}
	@${call log.var,compiler choices,$(developer.$(developer).compilers)}
	@${foreach \
            language, \
            $(languages),\
            ${call log.sec,"  $(language) options",}; \
            ${foreach \
                category, \
                $(languages.$(language).categories), \
                ${call log.var,$(category), $(developers.$(developer).$(language).$(category))}; \
            } \
        }


# end of file
