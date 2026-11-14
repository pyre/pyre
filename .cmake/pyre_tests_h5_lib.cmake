# -*- cmake -*-
# -*- coding: utf-8 -*-
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
# radar samples, their counts lined up with the members of the file by position
pyre_test_driver(tests/h5.lib/dataset_pairs.cc)
# a transfer through a compound that names a member the dataset lacks is refused, in each
# direction, while one that names some of its members reads just those
pyre_test_driver(tests/h5.lib/dataset_members_read.cc)
pyre_test_driver(tests/h5.lib/dataset_members_write.cc)
pyre_test_driver(tests/h5.lib/dataset_members_subset.cc)
# complex numbers whose parts the file names its own way, read by position
pyre_test_driver(tests/h5.lib/dataset_complex_members.cc)
# a strided tile read through the memory type deduced from the cells of the grid
pyre_test_driver(tests/h5.lib/dataset_read_deduced.cc)

# the drivers leave their scratch products behind so they can be inspected; the harness
# sweeps them, each after the driver that makes it
pyre_test_driver_cleanup(dataset_tiling.h5 tests/h5.lib/dataset_tiling.cc)
pyre_test_driver_cleanup(dataset_strided.h5 tests/h5.lib/dataset_strided.cc)
pyre_test_driver_cleanup(dataset_mosaic_write.h5 tests/h5.lib/dataset_mosaic_write.cc)
pyre_test_driver_cleanup(dataset_mosaic_read.h5 tests/h5.lib/dataset_mosaic_read.cc)
pyre_test_driver_cleanup(dataset_pairs.h5 tests/h5.lib/dataset_pairs.cc)
pyre_test_driver_cleanup(dataset_members_read.h5 tests/h5.lib/dataset_members_read.cc)
pyre_test_driver_cleanup(dataset_members_write.h5 tests/h5.lib/dataset_members_write.cc)
pyre_test_driver_cleanup(dataset_members_subset.h5 tests/h5.lib/dataset_members_subset.cc)
pyre_test_driver_cleanup(dataset_complex_members.h5 tests/h5.lib/dataset_complex_members.cc)
pyre_test_driver_cleanup(dataset_read_deduced.h5 tests/h5.lib/dataset_read_deduced.cc)


# end of file
