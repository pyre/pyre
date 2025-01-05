# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# compiler info
compilers.info:
	@${call log.sec,"compilers", "map of languages to compilers"}
	@${foreach language,$(languages),\
            ${call log.var,$(language),${call compiler.available,$(language)}} ;\
        }


# end of file
