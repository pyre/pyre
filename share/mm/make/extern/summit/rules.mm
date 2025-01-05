# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# display the summit configuration
extern.summit.info:
	@${call log.sec,"summit",}
	@${call log.var,"version",$(summit.version)}
	@${call log.var,"configuration file",$(summit.config)}
	@${call log.var,"home",$(summit.dir)}
	@${call log.var,"compiler flags",$(summit.flags)}
	@${call log.var,"defines",$(summit.defines)}
	@${call log.var,"incpath",$(summit.incpath)}
	@${call log.var,"linker flags",$(summit.ldflags)}
	@${call log.var,"libpath",$(summit.libpath)}
	@${call log.var,"libraries",$(summit.libraries)}
	@${call log.var,"dependencies",$(summit.dependencies)}
	@${call log.var,"c++ compile line",${call extern.compile.options,c++,summit}}
	@${call log.var,"c++ link line",${call extern.link.options,c++,summit}}


# end of file
