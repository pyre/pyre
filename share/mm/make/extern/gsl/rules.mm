# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# display the gsl configuration
extern.gsl.info:
	@${call log.sec,"gsl",}
	@${call log.var,"version",$(gsl.version)}
	@${call log.var,"blas",$(gsl.blas)}
	@${call log.var,"configuration file",$(gsl.config)}
	@${call log.var,"home",$(gsl.dir)}
	@${call log.var,"compiler flags",$(gsl.flags)}
	@${call log.var,"defines",$(gsl.defines)}
	@${call log.var,"incpath",$(gsl.incpath)}
	@${call log.var,"linker flags",$(gsl.ldflags)}
	@${call log.var,"libpath",$(gsl.libpath)}
	@${call log.var,"libraries",$(gsl.libraries)}
	@${call log.var,"dependencies",$(gsl.dependencies)}
	@${call log.var,"c++ compile line",${call extern.compile.options,c++,gsl}}
	@${call log.var,"c++ link line",${call extern.link.options,c++,gsl}}


# end of file
