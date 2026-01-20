# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# display the cspice configuration
extern.cspice.info:
	@${call log.sec,"cspice",}
	@${call log.var,"version",$(cspice.version)}
	@${call log.var,"configuration file",$(cspice.config)}
	@${call log.var,"home",$(cspice.dir)}
	@${call log.var,"compiler flags",$(cspice.flags)}
	@${call log.var,"defines",$(cspice.defines)}
	@${call log.var,"incpath",$(cspice.incpath)}
	@${call log.var,"linker flags",$(cspice.ldflags)}
	@${call log.var,"libpath",$(cspice.libpath)}
	@${call log.var,"libraries",$(cspice.libraries)}
	@${call log.var,"dependencies",$(cspice.dependencies)}
	@${call log.var,"c++ compile line",${call extern.compile.options,c++,cspice}}
	@${call log.var,"c++ link line",${call extern.link.options,c++,cspice}}


# end of file
