# -*- Makefile -*-
#
# libtorch rules for mm

extern.libtorch.info:
	@${call log.sec,"libtorch",}
	@${call log.var,"home",$(libtorch.dir)}
	@${call log.var,"incpath",$(libtorch.incpath)}
	@${call log.var,"compiler flags",$(libtorch.flags)}
	@${call log.var,"defines",$(libtorch.defines)}
	@${call log.var,"libpath",$(libtorch.libpath)}
	@${call log.var,"libraries",$(libtorch.libraries)}
	@${call log.var,"dependencies",$(libtorch.dependencies)}
	@${call log.var,"c++ compile line",${call extern.compile.options,c++,libtorch}}
	@${call log.var,"c++ link line",${call extern.link.options,c++,libtorch}}

# end of file
