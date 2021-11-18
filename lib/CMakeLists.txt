# -*- cmake -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2021 all rights reserved
#

# handle the portinfo file
pyre_portinfo()
# build libjournal
pyre_journalLib()
# build libpyre
pyre_pyreLib()
# and the mpi layers
pyre_mpiLib()

# end of file
