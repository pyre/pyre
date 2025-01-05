# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# display the numpy configuration
extern.numpy.info:
	@${call log.sec,"numpy",}
	@${call log.var,"version",$(numpy.version)}
	@${call log.var,"configuration file",$(numpy.config)}
	@${call log.var,"home",$(numpy.dir)}
	@${call log.var,"compiler flags",$(numpy.flags)}
	@${call log.var,"defines",$(numpy.defines)}
	@${call log.var,"incpath",$(numpy.incpath)}
	@${call log.var,"linker flags",$(numpy.ldflags)}
	@${call log.var,"libpath",$(numpy.libpath)}
	@${call log.var,"libraries",$(numpy.libraries)}
	@${call log.var,"dependencies",$(numpy.dependencies)}
	@${call log.var,"c++ compile line",${call extern.compile.options,c++,numpy}}
	@${call log.var,"c++ link line",${call extern.link.options,c++,numpy}}


# end of file
