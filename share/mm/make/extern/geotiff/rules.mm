# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# display the geotiff configuration
extern.geotiff.info:
	@${call log.sec,"geotiff",}
	@${call log.var,"version",$(geotiff.version)}
	@${call log.var,"configuration file",$(geotiff.config)}
	@${call log.var,"home",$(geotiff.dir)}
	@${call log.var,"compiler flags",$(geotiff.flags)}
	@${call log.var,"defines",$(geotiff.defines)}
	@${call log.var,"incpath",$(geotiff.incpath)}
	@${call log.var,"linker flags",$(geotiff.ldflags)}
	@${call log.var,"libpath",$(geotiff.libpath)}
	@${call log.var,"libraries",$(geotiff.libraries)}
	@${call log.var,"dependencies",$(geotiff.dependencies)}
	@${call log.var,"c++ compile line",${call extern.compile.options,c++,geotiff}}
	@${call log.var,"c++ link line",${call extern.link.options,c++,geotiff}}


# end of file
