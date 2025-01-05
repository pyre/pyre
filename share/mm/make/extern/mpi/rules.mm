# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# display the mpi configuration
extern.mpi.info:
	@${call log.sec,"mpi",}
	@${call log.var,"version",$(mpi.version)}
	@${call log.var,"flavor",$(mpi.flavor)}
	@${call log.var,"executive",$(mpi.executive)}
	@${call log.var,"configuration file",$(mpi.config)}
	@${call log.var,"home",$(mpi.dir)}
	@${call log.var,"compiler flags",$(mpi.flags)}
	@${call log.var,"defines",$(mpi.defines)}
	@${call log.var,"incpath",$(mpi.incpath)}
	@${call log.var,"linker flags",$(mpi.ldflags)}
	@${call log.var,"libpath",$(mpi.libpath)}
	@${call log.var,"libraries",$(mpi.libraries)}
	@${call log.var,"c++ compile line",${call extern.compile.options,c++,mpi}}
	@${call log.var,"c++ link line",${call extern.link.options,c++,mpi}}


# end of file
