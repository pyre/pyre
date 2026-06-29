# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# display the yaml-cpp configuration
extern.yaml-cpp.info:
	@${call log.sec,"yaml-cpp",}
	@${call log.var,"version",$(yaml-cpp.version)}
	@${call log.var,"configuration file",$(yaml-cpp.config)}
	@${call log.var,"home",$(yaml-cpp.dir)}
	@${call log.var,"compiler flags",$(yaml-cpp.flags)}
	@${call log.var,"defines",$(yaml-cpp.defines)}
	@${call log.var,"incpath",$(yaml-cpp.incpath)}
	@${call log.var,"linker flags",$(yaml-cpp.ldflags)}
	@${call log.var,"libpath",$(yaml-cpp.libpath)}
	@${call log.var,"libraries",$(yaml-cpp.libraries)}
	@${call log.var,"dependencies",$(yaml-cpp.dependencies)}
	@${call log.var,"c++ compile line",${call extern.compile.options,c++,yaml-cpp}}
	@${call log.var,"c++ link line",${call extern.link.options,c++,yaml-cpp}}


# end of file
