# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# display the kokkos configuration
extern.kokkos.info:
	@${call log.sec,"kokkos",}
	@${call log.var,"version",$(kokkos.version)}
	@${call log.var,"configuration file",$(kokkos.config)}
	@${call log.var,"home",$(kokkos.dir)}
	@${call log.var,"compiler flags",$(kokkos.flags)}
	@${call log.var,"defines",$(kokkos.defines)}
	@${call log.var,"incpath",$(kokkos.incpath)}
	@${call log.var,"linker flags",$(kokkos.ldflags)}
	@${call log.var,"libpath",$(kokkos.libpath)}
	@${call log.var,"libraries",$(kokkos.libraries)}
	@${call log.var,"c++ compile line",${call extern.compile.options,c++,kokkos}}
	@${call log.var,"c++ link line",${call extern.link.options,c++,kokkos}}


# end of file
