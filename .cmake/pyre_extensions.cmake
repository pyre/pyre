# -*- cmake -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2024 all rights reserved
#

# build the journal extension
pyre_journalModule()
# the host and timers extensions`
pyre_pyreModule()
# cuda
pyre_cudaModule()
# mpi
pyre_mpiModule()
# gsl
pyre_gslModule()
# h5
pyre_h5Module()
# postgres
pyre_postgresModule()

# end of file
