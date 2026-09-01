# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved

#
# h5 library: these drivers exercise the {pyre::h5} wrappers over the hdf5 c api without ever
# loading python, so a failure isolates the c++ layer from its bindings
#
# the plain {pyre_test_driver} is enough here: {libpyre} links hdf5 with the plain signature,
# so every driver inherits the headers and the library through the export interface
#
# sanity
pyre_test_driver(tests/h5.lib/sanity.cc)
# the datatype vocabulary the wrappers trade in
pyre_test_driver(tests/h5.lib/datatypes.cc)
# a dataspace describing its extent in the {pyre::grid} vocabulary
pyre_test_driver(tests/h5.lib/dataspace_packing.cc)
# a dataset's chunking, as the tiled layout a mosaic is assembled over
pyre_test_driver(tests/h5.lib/dataset_tiling.cc)
# reading and writing a tile that visits only every n-th cell along each axis
pyre_test_driver(tests/h5.lib/dataset_strided.cc)
# the out-of-core mosaic, in each direction
pyre_test_driver(tests/h5.lib/dataset_mosaic_write.cc)
pyre_test_driver(tests/h5.lib/dataset_mosaic_read.cc)

# the drivers leave their scratch products behind so they can be inspected; the harness
# sweeps them, each after the driver that makes it
pyre_test_driver_cleanup(dataset_tiling.h5 tests/h5.lib/dataset_tiling.cc)
pyre_test_driver_cleanup(dataset_strided.h5 tests/h5.lib/dataset_strided.cc)
pyre_test_driver_cleanup(dataset_mosaic_write.h5 tests/h5.lib/dataset_mosaic_write.cc)
pyre_test_driver_cleanup(dataset_mosaic_read.h5 tests/h5.lib/dataset_mosaic_read.cc)


# end of file
