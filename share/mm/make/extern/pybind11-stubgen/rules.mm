# -*- makefile -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# display the pybind11-stubgen configuration
extern.pybind11-stubgen.info:
	@${call log.sec,"pybind11-stubgen",}
	@${call log.var,"version",$(pybind11-stubgen.version)}
	@${call log.var,"configuration file",$(pybind11-stubgen.config)}
	@${call log.var,"home",$(pybind11-stubgen.dir)}
	@${call log.var,"module markers",$(pybind11-stubgen.markers.modules)}
	@${call log.var,"driver",$(pybind11-stubgen.driver)}


# end of file
