# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# target info
targets.info:
	@${call log.sec,"target", "target info"}
	@${call log.var,"      tag",$(target.tag)}
	@${call log.var," variants",$(target.variants)}
	@${call log.var,"compilers",$(target.compilers)}

# make a rule to show taret specific info
#  usage: target.info.flags
define target.info.flags
#
targets.$(1).info:
	@${call log.sec,$(1),$(targets.$(1).description)}
	@${foreach language,$(languages),\
            ${if ${value compiler.$(language)}, \
                ${call log.sec,"  $(language)",$(compiler.$(language))}; \
                ${foreach \
                    category,  \
                    $(languages.$(language).categories), \
                    ${call log.var,$(category),$(targets.$(1).$(language).$(category))}; \
                } \
            } \
        }
#
endef


# end of file
