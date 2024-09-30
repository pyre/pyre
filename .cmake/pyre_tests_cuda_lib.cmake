# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


#
# pyre
#

# cuda tests managed memory
pyre_test_driver_cuda(tests/cuda.lib/managed.cc)
pyre_test_driver_cuda(tests/cuda.lib/grid_managed_sanity.cc)

# cuda tests pinned memory
pyre_test_driver_cuda(tests/cuda.lib/pinned.cc)
pyre_test_driver_cuda(tests/cuda.lib/grid_pinned_sanity.cc)

# cuda tests mapped memory
pyre_test_driver_cuda(tests/cuda.lib/mapped.cc)
pyre_test_driver_cuda(tests/cuda.lib/grid_mapped_sanity.cc)

# end of file
