# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# display the cgal configuration
extern.cgal.info:
	@${call log.sec,"cgal",}
	@${call log.var,"version",$(cgal.version)}
	@${call log.var,"configuration file",$(cgal.config)}
	@${call log.var,"home",$(cgal.dir)}
	@${call log.var,"compiler flags",$(cgal.flags)}
	@${call log.var,"defines",$(cgal.defines)}
	@${call log.var,"incpath",$(cgal.incpath)}
	@${call log.var,"linker flags",$(cgal.ldflags)}
	@${call log.var,"libpath",$(cgal.libpath)}
	@${call log.var,"libraries",$(cgal.libraries)}
	@${call log.var,"dependencies",$(cgal.dependencies)}
	@${call log.var,"c++ compile line",${call extern.compile.options,c++,cgal}}
	@${call log.var,"c++ link line",${call extern.link.options,c++,cgal}}


# end of file
