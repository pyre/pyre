# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# display the summit configuration
extern.sundials.info:
	@${call log.sec,"sundials",}
	@${call log.var,"version",$(sundials.version)}
	@${call log.var,"configuration file",$(sundials.config)}
	@${call log.var,"home",$(sundials.dir)}
	@${call log.var,"compiler flags",$(sundials.flags)}
	@${call log.var,"defines",$(sundials.defines)}
	@${call log.var,"incpath",$(sundials.incpath)}
	@${call log.var,"linker flags",$(sundials.ldflags)}
	@${call log.var,"libpath",$(sundials.libpath)}
	@${call log.var,"libraries",$(sundials.libraries)}
	@${call log.var,"dependencies",$(sundials.dependencies)}
	@${call log.var,"c++ compile line",${call extern.compile.options,c++,sundials}}
	@${call log.var,"c++ link line",${call extern.link.options,c++,sundials}}


# end of file
