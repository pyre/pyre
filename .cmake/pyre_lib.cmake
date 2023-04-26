# -*- cmake -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2023 all rights reserved
#

# handle the portinfo file
pyre_portinfo()
# build libjournal
pyre_journalLib()
# build libpyre
pyre_pyreLib()
# and the cuda layers
pyre_cudaLib()
# and the mpi layers
pyre_mpiLib()

# end of file
