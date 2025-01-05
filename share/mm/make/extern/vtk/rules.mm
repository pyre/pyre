# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# display the vtk configuration
extern.vtk.info:
	@${call log.sec,"vtk",}
	@${call log.var,"version",$(vtk.version)}
	@${call log.var,"configuration file",$(vtk.config)}
	@${call log.var,"home",$(vtk.dir)}
	@${call log.var,"compiler flags",$(vtk.flags)}
	@${call log.var,"defines",$(vtk.defines)}
	@${call log.var,"incpath",$(vtk.incpath)}
	@${call log.var,"linker flags",$(vtk.flags)}
	@${call log.var,"libpath",$(vtk.libpath)}
	@${call log.var,"requested libraries",$(vtk.required)}
	@${call log.var,"transformed libraries",$(vtk.libraries)}
	@${call log.var,"c++ compile line",${call extern.compile.options,c++,vtk}}
	@${call log.var,"c++ link line",${call extern.link.options,c++,vtk}}


# end of file
