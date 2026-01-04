# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# display the slepc configuration
extern.slepc.info:
	@${call log.sec,"slepc",}
	@${call log.var,"version",$(slepc.version)}
	@${call log.var,"configuration file",$(slepc.config)}
	@${call log.var,"home",$(slepc.dir)}
	@${call log.var,"compiler flags",$(slepc.flags)}
	@${call log.var,"defines",$(slepc.defines)}
	@${call log.var,"incpath",$(slepc.incpath)}
	@${call log.var,"linker flags",$(slepc.ldflags)}
	@${call log.var,"libpath",$(slepc.libpath)}
	@${call log.var,"libraries",$(slepc.libraries)}
	@${call log.var,"dependencies",$(slepc.dependencies)}
	@${call log.var,"c++ compile line",${call extern.compile.options,c++,slepc}}
	@${call log.var,"c++ link line",${call extern.link.options,c++,slepc}}


# end of file
