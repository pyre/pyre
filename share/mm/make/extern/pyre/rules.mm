# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# display the pyre configuration
extern.pyre.info:
	@${call log.sec,"pyre",}
	@${call log.var,"version",$(pyre.version)}
	@${call log.var,"configuration file",$(pyre.config)}
	@${call log.var,"home",$(pyre.dir)}
	@${call log.var,"compiler flags",$(pyre.flags)}
	@${call log.var,"defines",$(pyre.defines)}
	@${call log.var,"incpath",$(pyre.incpath)}
	@${call log.var,"linker flags",$(pyre.ldflags)}
	@${call log.var,"libpath",$(pyre.libpath)}
	@${call log.var,"libraries",$(pyre.libraries)}
	@${call log.var,"dependencies",$(pyre.dependencies)}
	@${call log.var,"c++ compile line",${call extern.compile.options,c++,pyre}}
	@${call log.var,"c++ link line",${call extern.link.options,c++,pyre}}


# end of file
