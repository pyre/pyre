# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# display the openblas configuration
extern.openblas.info:
	@${call log.sec,"openblas",}
	@${call log.var,"version",$(openblas.version)}
	@${call log.var,"blas",$(openblas.blas)}
	@${call log.var,"configuration file",$(openblas.config)}
	@${call log.var,"home",$(openblas.dir)}
	@${call log.var,"compiler flags",$(openblas.flags)}
	@${call log.var,"defines",$(openblas.defines)}
	@${call log.var,"incpath",$(openblas.incpath)}
	@${call log.var,"linker flags",$(openblas.ldflags)}
	@${call log.var,"libpath",$(openblas.libpath)}
	@${call log.var,"libraries",$(openblas.libraries)}
	@${call log.var,"c++ compile line",${call extern.compile.options,c++,openblas}}
	@${call log.var,"c++ link line",${call extern.link.options,c++,openblas}}


# end of file
