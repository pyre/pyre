# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# display the parmetis configuration
extern.parmetis.info:
	@${call log.sec,"parmetis",}
	@${call log.var,"version",$(parmetis.version)}
	@${call log.var,"configuration file",$(parmetis.config)}
	@${call log.var,"home",$(parmetis.dir)}
	@${call log.var,"compiler flags",$(parmetis.flags)}
	@${call log.var,"defines",$(parmetis.defines)}
	@${call log.var,"incpath",$(parmetis.incpath)}
	@${call log.var,"linker flags",$(parmetis.ldflags)}
	@${call log.var,"libpath",$(parmetis.libpath)}
	@${call log.var,"libraries",$(parmetis.libraries)}
	@${call log.var,"dependencies",$(parmetis.dependencies)}
	@${call log.var,"c++ compile line",${call extern.compile.options,c++,parmetis}}
	@${call log.var,"c++ link line",${call extern.link.options,c++,parmetis}}


# end of file
