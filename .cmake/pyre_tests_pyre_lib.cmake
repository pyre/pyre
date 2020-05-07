# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2020 all rights reserved
#


#
# pyre
#

# algebra
pyre_test_driver(pyre.lib/algebra/bcd.cc)

# geometry
pyre_test_driver(pyre.lib/geometry/point.cc)
pyre_test_driver(pyre.lib/geometry/pointcloud.cc)
pyre_test_driver(pyre.lib/geometry/brick.cc)

# grid
pyre_test_driver(pyre.lib/grid/index.cc)
pyre_test_driver(pyre.lib/grid/index-access.cc)
pyre_test_driver(pyre.lib/grid/index-bool.cc)
pyre_test_driver(pyre.lib/grid/index-arithmetic.cc)
pyre_test_driver(pyre.lib/grid/packing.cc)
pyre_test_driver(pyre.lib/grid/packing-c.cc)
pyre_test_driver(pyre.lib/grid/packing-fortran.cc)
pyre_test_driver(pyre.lib/grid/packing-access.cc)
pyre_test_driver(pyre.lib/grid/slice.cc)
pyre_test_driver(pyre.lib/grid/iterator.cc)
pyre_test_driver(pyre.lib/grid/iterator-access.cc)
pyre_test_driver(pyre.lib/grid/iterator-loop.cc)
pyre_test_driver(pyre.lib/grid/iterator-slice.cc)
pyre_test_driver(pyre.lib/grid/layout.cc)
pyre_test_driver(pyre.lib/grid/layout-order.cc)
pyre_test_driver(pyre.lib/grid/layout-order-default.cc)
pyre_test_driver(pyre.lib/grid/layout-slice.cc)

pyre_test_driver(pyre.lib/grid/grid-view.cc)
pyre_test_driver(pyre.lib/grid/grid-heap.cc)
pyre_test_driver(pyre.lib/grid/grid-direct.cc)
pyre_test_driver(pyre.lib/grid/grid-direct-data.cc)
pyre_test_driver(pyre.lib/grid/grid-direct-set.cc)
pyre_test_driver(pyre.lib/grid/grid-direct-get.cc)
pyre_test_driver(pyre.lib/grid/grid-fill.cc)
pyre_test_driver(pyre.lib/grid/grid-mosaic.cc)
pyre_test_driver(pyre.lib/grid/grid-scan.cc)
pyre_test_driver(pyre.lib/grid/grid-transform.cc)
pyre_test_driver(pyre.lib/grid/grid-view-assignment.cc)
# the {grid-direct} tests need cleanup
add_test(NAME pyre.lib.grid.grid-direct.cleanup
  COMMAND ${BASH_PROGRAM} -c "rm grid.dat"
  )
# and they need to happen in a spcific order
set_property(TEST pyre.lib.grid.grid-direct-data.cc PROPERTY
  DEPENDS pyre.lib.grid.grid-direct.cc
  )
set_property(TEST pyre.lib.grid.grid-direct-set.cc PROPERTY
  DEPENDS pyre.lib.grid.grid-direct-data.cc
  )
set_property(TEST pyre.lib.grid.grid-direct-get.cc PROPERTY
  DEPENDS pyre.lib.grid.grid-direct-set.cc
  )
set_property(TEST pyre.lib.grid.grid-direct.cleanup PROPERTY
  DEPENDS pyre.lib.grid.grid-direct-get.cc
  )


# memory
pyre_test_driver(pyre.lib/memory/view-instantiate.cc)
pyre_test_driver(pyre.lib/memory/constview-instantiate.cc)
pyre_test_driver(pyre.lib/memory/heap-instantiate.cc)

pyre_test_driver(pyre.lib/memory/direct-create.cc)
pyre_test_driver(pyre.lib/memory/direct-map.cc)
pyre_test_driver(pyre.lib/memory/direct-instantiate.cc)
pyre_test_driver(pyre.lib/memory/direct-instantiate-partial.cc)
# the {direct} test cases need cleanup
add_test(NAME pyre.lib.memory.direct.cleanup
  COMMAND ${BASH_PROGRAM} -c "rm direct-grid.dat"
  )
# and they need to happen in a spcific order
set_property(TEST pyre.lib.memory.direct-map.cc PROPERTY
  DEPENDS pyre.lib.memory.direct-create.cc
  )
set_property(TEST pyre.lib.memory.direct-instantiate.cc PROPERTY
  DEPENDS pyre.lib.memory.direct-map.cc
  )
set_property(TEST pyre.lib.memory.direct-instantiate-partial.cc PROPERTY
  DEPENDS pyre.lib.memory.direct-instantiate.cc
  )
set_property(TEST pyre.lib.memory.direct.cleanup PROPERTY
  DEPENDS pyre.lib.memory.direct-instantiate-partial.cc
  )

pyre_test_driver(pyre.lib/memory/constdirect-create.cc)
pyre_test_driver(pyre.lib/memory/constdirect-map.cc)
pyre_test_driver(pyre.lib/memory/constdirect-instantiate.cc)
pyre_test_driver(pyre.lib/memory/constdirect-instantiate-partial.cc)
# the {constdirect} test cases need cleanup
add_test(NAME pyre.lib.memory.constdirect.cleanup
  COMMAND ${BASH_PROGRAM} -c "rm constdirect-grid.dat"
  )
# and they need to happen in a spcific order
set_property(TEST pyre.lib.memory.constdirect-map.cc PROPERTY
  DEPENDS pyre.lib.memory.constdirect-create.cc
  )
set_property(TEST pyre.lib.memory.constdirect-instantiate.cc PROPERTY
  DEPENDS pyre.lib.memory.constdirect-map.cc
  )
set_property(TEST pyre.lib.memory.constdirect-instantiate-partial.cc PROPERTY
  DEPENDS pyre.lib.memory.constdirect-instantiate.cc
  )
set_property(TEST pyre.lib.memory.constdirect.cleanup PROPERTY
  DEPENDS pyre.lib.memory.constdirect-instantiate-partial.cc
  )


# timers
pyre_test_driver(pyre.lib/timers/timer.cc)


# end of file
