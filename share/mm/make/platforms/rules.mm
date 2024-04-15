# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# platform info
platform.info:
	@${call log.sec,"platform","platform info"}
	@${call log.var,os,$(platform.os)}
	@${call log.var,architecture,$(platform.arch)}
	@${call log.var,tag,$(platform)}
	@${call log.var,macro,$(platform.macro)}
	@${foreach language, $(languages), \
		${call log.sec,$(language),}; \
		${foreach category, $(languages.$(language).categories), \
			${call log.var,platform.$(language).$(category),$(platform.$(language).$(category))}; \
		} \
	}



# end of file
