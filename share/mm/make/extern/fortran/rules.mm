# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# display the fortran configuration
extern.fortran.info:
	@${call log.sec,"fortran",}
	@${call log.var,"version",$(fortran.version)}
	@${call log.var,"configuration file",$(fortran.config)}
	@${call log.var,"home",$(fortran.dir)}
	@${call log.var,"compiler flags",$(fortran.flags)}
	@${call log.var,"defines",$(fortran.defines)}
	@${call log.var,"incpath",$(fortran.incpath)}
	@${call log.var,"linker flags",$(fortran.ldflags)}
	@${call log.var,"libpath",$(fortran.libpath)}
	@${call log.var,"libraries",$(fortran.libraries)}
	@${call log.var,"dependencies",$(fortran.dependencies)}
	@${call log.var,"c++ compile line",${call extern.compile.options,c++,fortran}}
	@${call log.var,"c++ link line",${call extern.link.options,c++,fortran}}


# end of file
