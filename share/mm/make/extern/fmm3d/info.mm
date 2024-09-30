# -*- Makefile -*-
#
# michael a.g. aïvázis
# parasim
# (c) 1998-2023 all rights reserved
#

# show me
# ${info -- fmm3d.info}

# display the summit configuration
extern.fmm3d.info:
	@${call log.sec,"fmm3d",}
	@${call log.var,"version",$(fmm3d.version)}
	@${call log.var,"configuration file",$(fmm3d.config)}
	@${call log.var,"home",$(fmm3d.dir)}
	@${call log.var,"compiler flags",$(fmm3d.flags)}
	@${call log.var,"defines",$(fmm3d.defines)}
	@${call log.var,"incpath",$(fmm3d.incpath)}
	@${call log.var,"linker flags",$(fmm3d.ldflags)}
	@${call log.var,"libpath",$(fmm3d.libpath)}
	@${call log.var,"libraries",$(fmm3d.libraries)}
	@${call log.var,"dependencies",$(fmm3d.dependencies)}
	@${call log.var,"c++ compile line",${call extern.compile.options,c++,fmm3d}}
	@${call log.var,"c++ link line",${call extern.link.options,c++,fmm3d}}

# show me
# ${info -- done with fmm3d.info}

# end of file
