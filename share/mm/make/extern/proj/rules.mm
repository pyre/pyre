# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# display the proj configuration
extern.proj.info:
	@${call log.sec,"proj",}
	@${call log.var,"version",$(proj.version)}
	@${call log.var,"configuration file",$(proj.config)}
	@${call log.var,"home",$(proj.dir)}
	@${call log.var,"compiler flags",$(proj.flags)}
	@${call log.var,"defines",$(proj.defines)}
	@${call log.var,"incpath",$(proj.incpath)}
	@${call log.var,"linker flags",$(proj.ldflags)}
	@${call log.var,"libpath",$(proj.libpath)}
	@${call log.var,"libraries",$(proj.libraries)}
	@${call log.var,"dependencies",$(proj.dependencies)}
	@${call log.var,"c++ compile line",${call extern.compile.options,c++,proj}}
	@${call log.var,"c++ link line",${call extern.link.options,c++,proj}}


# end of file
