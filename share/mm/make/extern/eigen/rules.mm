# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# display the eigen configuration
extern.eigen.info:
	@${call log.sec,"eigen",}
	@${call log.var,"version",$(eigen.version)}
	@${call log.var,"configuration file",$(eigen.config)}
	@${call log.var,"home",$(eigen.dir)}
	@${call log.var,"compiler flags",$(eigen.flags)}
	@${call log.var,"defines",$(eigen.defines)}
	@${call log.var,"incpath",$(eigen.incpath)}
	@${call log.var,"linker flags",$(eigen.ldflags)}
	@${call log.var,"libpath",$(eigen.libpath)}
	@${call log.var,"libraries",$(eigen.libraries)}
	@${call log.var,"dependencies",$(eigen.dependencies)}
	@${call log.var,"c++ compile line",${call extern.compile.options,c++,eigen}}
	@${call log.var,"c++ link line",${call extern.link.options,c++,eigen}}


# end of file
