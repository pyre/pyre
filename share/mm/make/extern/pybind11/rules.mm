# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# display the pybind11 configuration
extern.pybind11.info:
	@${call log.sec,"pybind11",}
	@${call log.var,"version",$(pybind11.version)}
	@${call log.var,"configuration file",$(pybind11.config)}
	@${call log.var,"home",$(pybind11.dir)}
	@${call log.var,"compiler flags",$(pybind11.flags)}
	@${call log.var,"defines",$(pybind11.defines)}
	@${call log.var,"incpath",$(pybind11.incpath)}
	@${call log.var,"dependencies",$(pybind11.dependencies)}
	@${call log.var,"c++ compile line",${call extern.compile.options,c++,pybind11}}
	@${call log.var,"c++ link line",${call extern.link.options,c++,pybind11}}


# end of file
