# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# display the summit configuration
extern.fmt.info:
	@${call log.sec,"fmt",}
	@${call log.var,"version",$(fmt.version)}
	@${call log.var,"configuration file",$(fmt.config)}
	@${call log.var,"home",$(fmt.dir)}
	@${call log.var,"compiler flags",$(fmt.flags)}
	@${call log.var,"defines",$(fmt.defines)}
	@${call log.var,"incpath",$(fmt.incpath)}
	@${call log.var,"linker flags",$(fmt.ldflags)}
	@${call log.var,"libpath",$(fmt.libpath)}
	@${call log.var,"libraries",$(fmt.libraries)}
	@${call log.var,"dependencies",$(fmt.dependencies)}
	@${call log.var,"c++ compile line",${call extern.compile.options,c++,fmt}}
	@${call log.var,"c++ link line",${call extern.link.options,c++,fmt}}


# end of file
