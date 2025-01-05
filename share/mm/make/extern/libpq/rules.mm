# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# display the libpq configuration
extern.libpq.info:
	@${call log.sec,"libpq",}
	@${call log.var,"version",$(libpq.version)}
	@${call log.var,"configuration file",$(libpq.config)}
	@${call log.var,"home",$(libpq.dir)}
	@${call log.var,"compiler flags",$(libpq.flags)}
	@${call log.var,"defines",$(libpq.defines)}
	@${call log.var,"incpath",$(libpq.incpath)}
	@${call log.var,"linker flags",$(libpq.ldflags)}
	@${call log.var,"libpath",$(libpq.libpath)}
	@${call log.var,"libraries",$(libpq.libraries)}
	@${call log.var,"dependencies",$(libpq.dependencies)}
	@${call log.var,"c++ compile line",${call extern.compile.options,c++,libpq}}
	@${call log.var,"c++ link line",${call extern.link.options,c++,libpq}}


# end of file
