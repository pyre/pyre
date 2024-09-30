# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# display the gdal configuration
extern.gdal.info:
	@${call log.sec,"gdal",}
	@${call log.var,"version",$(gdal.version)}
	@${call log.var,"configuration file",$(gdal.config)}
	@${call log.var,"home",$(gdal.dir)}
	@${call log.var,"compiler flags",$(gdal.flags)}
	@${call log.var,"defines",$(gdal.defines)}
	@${call log.var,"incpath",$(gdal.incpath)}
	@${call log.var,"linker flags",$(gdal.ldflags)}
	@${call log.var,"libpath",$(gdal.libpath)}
	@${call log.var,"libraries",$(gdal.libraries)}
	@${call log.var,"dependencies",$(gdal.dependencies)}
	@${call log.var,"c++ compile line",${call extern.compile.options,c++,gdal}}
	@${call log.var,"c++ link line",${call extern.link.options,c++,gdal}}


# end of file
