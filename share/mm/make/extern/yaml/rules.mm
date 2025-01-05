# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# display the yaml configuration
extern.yaml.info:
	@${call log.sec,"yaml",}
	@${call log.var,"version",$(yaml.version)}
	@${call log.var,"configuration file",$(yaml.config)}
	@${call log.var,"home",$(yaml.dir)}
	@${call log.var,"compiler flags",$(yaml.flags)}
	@${call log.var,"defines",$(yaml.defines)}
	@${call log.var,"incpath",$(yaml.incpath)}
	@${call log.var,"linker flags",$(yaml.ldflags)}
	@${call log.var,"libpath",$(yaml.libpath)}
	@${call log.var,"libraries",$(yaml.libraries)}
	@${call log.var,"dependencies",$(yaml.dependencies)}
	@${call log.var,"c++ compile line",${call extern.compile.options,c++,yaml}}
	@${call log.var,"c++ link line",${call extern.link.options,c++,yaml}}


# end of file
