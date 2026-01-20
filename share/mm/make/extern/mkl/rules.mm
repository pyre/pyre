# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# display the mkl configuration
extern.mkl.info:
	@${call log.sec,"mkl",}
	@${call log.var,"version",$(mkl.version)}
	@${call log.var,"configuration file",$(mkl.config)}
	@${call log.var,"home",$(mkl.dir)}
	@${call log.var,"compiler flags",$(mkl.flags)}
	@${call log.var,"defines",$(mkl.defines)}
	@${call log.var,"incpath",$(mkl.incpath)}
	@${call log.var,"linker flags",$(mkl.ldflags)}
	@${call log.var,"libpath",$(mkl.libpath)}
	@${call log.var,"libraries",$(mkl.libraries)}
	@${call log.var,"c++ compile line",${call extern.compile.options,c++,mkl}}
	@${call log.var,"c++ link line",${call extern.link.options,c++,mkl}}


# end of file
