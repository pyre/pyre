# -*- cmake -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2026 all rights reserved
#

# handle the portinfo file
pyre_portinfo()
# build libjournal
pyre_journalLib()
# build libpyre
pyre_pyreLib()
# add the pyre::h5 wrappers to libpyre when hdf5 is available
pyre_h5Lib()
# and the cuda layers
pyre_cudaLib()
# and the mpi layers
pyre_mpiLib()

# end of file
