# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# display the summit configuration
extern.cantera.info:
	@${call log.sec,"cantera",}
	@${call log.var,"version",$(cantera.version)}
	@${call log.var,"configuration file",$(cantera.config)}
	@${call log.var,"home",$(cantera.dir)}
	@${call log.var,"compiler flags",$(cantera.flags)}
	@${call log.var,"defines",$(cantera.defines)}
	@${call log.var,"incpath",$(cantera.incpath)}
	@${call log.var,"linker flags",$(cantera.ldflags)}
	@${call log.var,"libpath",$(cantera.libpath)}
	@${call log.var,"libraries",$(cantera.libraries)}
	@${call log.var,"dependencies",$(cantera.dependencies)}
	@${call log.var,"c++ compile line",${call extern.compile.options,c++,cantera}}
	@${call log.var,"c++ link line",${call extern.link.options,c++,cantera}}


# end of file
