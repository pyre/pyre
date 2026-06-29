# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# display the catch2 configuration
extern.catch2.info:
	@${call log.sec,"catch2",}
	@${call log.var,"version",$(catch2.version)}
	@${call log.var,"configuration file",$(catch2.config)}
	@${call log.var,"home",$(catch2.dir)}
	@${call log.var,"compiler flags",$(catch2.flags)}
	@${call log.var,"defines",$(catch2.defines)}
	@${call log.var,"incpath",$(catch2.incpath)}
	@${call log.var,"linker flags",$(catch2.ldflags)}
	@${call log.var,"libpath",$(catch2.libpath)}
	@${call log.var,"libraries",$(catch2.libraries)}
	@${call log.var,"dependencies",$(catch2.dependencies)}
	@${call log.var,"c++ compile line",${call extern.compile.options,c++,catch2}}
	@${call log.var,"c++ link line",${call extern.link.options,c++,catch2}}


# end of file
