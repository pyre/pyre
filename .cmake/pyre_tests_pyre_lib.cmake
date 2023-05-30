# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


#
# pyre
#

# algebra
pyre_test_driver(tests/pyre.lib/algebra/bcd.cc)


# geometry
pyre_test_driver(tests/pyre.lib/geometry/point.cc)
pyre_test_driver(tests/pyre.lib/geometry/pointcloud.cc)
pyre_test_driver(tests/pyre.lib/geometry/brick.cc)


# grid
pyre_test_driver(tests/pyre.lib/grid/canonical_box.cc)
pyre_test_driver(tests/pyre.lib/grid/canonical_box_skip.cc)
pyre_test_driver(tests/pyre.lib/grid/canonical_cslice.cc)
pyre_test_driver(tests/pyre.lib/grid/canonical_map.cc)
pyre_test_driver(tests/pyre.lib/grid/canonical_map_origin.cc)
pyre_test_driver(tests/pyre.lib/grid/canonical_map_positive.cc)
pyre_test_driver(tests/pyre.lib/grid/canonical_nudge.cc)
pyre_test_driver(tests/pyre.lib/grid/canonical_sanity.cc)
pyre_test_driver(tests/pyre.lib/grid/canonical_slice.cc)
pyre_test_driver(tests/pyre.lib/grid/canonical_visit.cc)
pyre_test_driver(tests/pyre.lib/grid/canonical_visit_order.cc)
pyre_test_driver(tests/pyre.lib/grid/grid_heap_box.cc)
pyre_test_driver(tests/pyre.lib/grid/grid_heap_box_skip.cc)
pyre_test_driver(tests/pyre.lib/grid/grid_heap_expand.cc)
pyre_test_driver(tests/pyre.lib/grid/grid_heap_iteration.cc)
pyre_test_driver(tests/pyre.lib/grid/grid_heap_sanity.cc)
pyre_test_driver(tests/pyre.lib/grid/grid_mmap_get.cc)
pyre_test_driver(tests/pyre.lib/grid/grid_mmap_sanity.cc)
pyre_test_driver(tests/pyre.lib/grid/grid_mmap_set.cc)
pyre_test_driver(tests/pyre.lib/grid/grid_sat.cc)
pyre_test_driver(tests/pyre.lib/grid/grid_sat_box.cc)
pyre_test_driver(tests/pyre.lib/grid/index_access.cc)
pyre_test_driver(tests/pyre.lib/grid/index_arithmetic.cc)
pyre_test_driver(tests/pyre.lib/grid/index_cartesian.cc)
pyre_test_driver(tests/pyre.lib/grid/index_enum.cc)
pyre_test_driver(tests/pyre.lib/grid/index_fill.cc)
pyre_test_driver(tests/pyre.lib/grid/index_from_tuple.cc)
pyre_test_driver(tests/pyre.lib/grid/index_iterator.cc)
pyre_test_driver(tests/pyre.lib/grid/index_sanity.cc)
pyre_test_driver(tests/pyre.lib/grid/index_scaling.cc)
pyre_test_driver(tests/pyre.lib/grid/index_structured_binding.cc)
pyre_test_driver(tests/pyre.lib/grid/index_zero.cc)
pyre_test_driver(tests/pyre.lib/grid/order_access.cc)
pyre_test_driver(tests/pyre.lib/grid/order_c.cc)
pyre_test_driver(tests/pyre.lib/grid/order_fortran.cc)
pyre_test_driver(tests/pyre.lib/grid/order_sanity.cc)
pyre_test_driver(tests/pyre.lib/grid/product_access.cc)
pyre_test_driver(tests/pyre.lib/grid/product_iteration.cc)
pyre_test_driver(tests/pyre.lib/grid/product_ordered_iteration.cc)
pyre_test_driver(tests/pyre.lib/grid/product_sanity.cc)
pyre_test_driver(tests/pyre.lib/grid/rep_at.cc)
pyre_test_driver(tests/pyre.lib/grid/rep_eq.cc)
pyre_test_driver(tests/pyre.lib/grid/rep_fill.cc)
pyre_test_driver(tests/pyre.lib/grid/rep_iteration.cc)
pyre_test_driver(tests/pyre.lib/grid/rep_op.cc)
pyre_test_driver(tests/pyre.lib/grid/rep_reverse_iteration.cc)
pyre_test_driver(tests/pyre.lib/grid/rep_sanity.cc)
pyre_test_driver(tests/pyre.lib/grid/rep_zero.cc)
pyre_test_driver(tests/pyre.lib/grid/sanity.cc)
pyre_test_driver(tests/pyre.lib/grid/shape_access.cc)
pyre_test_driver(tests/pyre.lib/grid/shape_arithmetic.cc)
pyre_test_driver(tests/pyre.lib/grid/shape_cartesian.cc)
pyre_test_driver(tests/pyre.lib/grid/shape_sanity.cc)
pyre_test_driver(tests/pyre.lib/grid/shape_scaling.cc)
pyre_test_driver(tests/pyre.lib/grid/shape_structured_binding.cc)

# the {grid_get} tests need cleanup
add_test(NAME tests.pyre.lib.grid.grid_mmap.cleanup
  COMMAND ${BASH_PROGRAM} -c "rm grid_mmap.data"
  )

# and they need to happen in a specific order
set_property(TEST tests.pyre.lib.grid.grid_mmap_set.cc PROPERTY
  DEPENDS tests.pyre.lib.grid.grid_mmap_sanity.cc
  )
set_property(TEST tests.pyre.lib.grid.grid_mmap_get.cc PROPERTY
  DEPENDS tests.pyre.lib.grid.grid_mmap_set.cc
  )
set_property(TEST tests.pyre.lib.grid.grid_mmap.cleanup PROPERTY
  DEPENDS tests.pyre.lib.grid.grid_mmap_get.cc
  )


# memory
pyre_test_driver(tests/pyre.lib/memory/constmap_oob.cc)
pyre_test_driver(tests/pyre.lib/memory/constmap_read.cc)
pyre_test_driver(tests/pyre.lib/memory/constview_access.cc)
pyre_test_driver(tests/pyre.lib/memory/filemap_create.cc)
pyre_test_driver(tests/pyre.lib/memory/filemap_read.cc)
pyre_test_driver(tests/pyre.lib/memory/filemap_write.cc)
pyre_test_driver(tests/pyre.lib/memory/heap_access.cc)
pyre_test_driver(tests/pyre.lib/memory/heap_borrow.cc)
pyre_test_driver(tests/pyre.lib/memory/heap_copy.cc)
pyre_test_driver(tests/pyre.lib/memory/heap_oob.cc)
pyre_test_driver(tests/pyre.lib/memory/map_create.cc)
pyre_test_driver(tests/pyre.lib/memory/map_oob.cc)
pyre_test_driver(tests/pyre.lib/memory/map_read.cc)
pyre_test_driver(tests/pyre.lib/memory/map_write.cc)
pyre_test_driver(tests/pyre.lib/memory/memory_sanity.cc)
pyre_test_driver(tests/pyre.lib/memory/view_access.cc)
pyre_test_driver(tests/pyre.lib/memory/view_oob.cc)

# some tests require cleanup
add_test(NAME tests.pyre.lib.memory.filemap.cleanup
  COMMAND ${BASH_PROGRAM} -c "rm filemap.dat"
  )
add_test(NAME tests.pyre.lib.memory.map.cleanup
  COMMAND ${BASH_PROGRAM} -c "rm map.dat"
  )

# some tests must happen in a specific order
set_property(TEST tests.pyre.lib.memory.filemap_write.cc PROPERTY
  DEPENDS tests.pyre.lib.memory.filemap_create.cc
  )
set_property(TEST tests.pyre.lib.memory.filemap_read.cc PROPERTY
  DEPENDS tests.pyre.lib.memory.filemap_write.cc
  )
set_property(TEST tests.pyre.lib.memory.filemap.cleanup PROPERTY
  DEPENDS tests.pyre.lib.memory.filemap_read.cc
  )

set_property(TEST tests.pyre.lib.memory.map_write.cc PROPERTY
  DEPENDS tests.pyre.lib.memory.map_create.cc
  )
set_property(TEST tests.pyre.lib.memory.map_read.cc PROPERTY
  DEPENDS tests.pyre.lib.memory.map_write.cc
  )
set_property(TEST tests.pyre.lib.memory.map_oob.cc PROPERTY
  DEPENDS tests.pyre.lib.memory.map_write.cc
  )
set_property(TEST tests.pyre.lib.memory.constmap_read.cc PROPERTY
  DEPENDS tests.pyre.lib.memory.map_write.cc
  )
set_property(TEST tests.pyre.lib.memory.constmap_oob.cc PROPERTY
  DEPENDS tests.pyre.lib.memory.map_write.cc
  )
set_property(TEST tests.pyre.lib.memory.map.cleanup PROPERTY
  DEPENDS
      tests.pyre.lib.memory.map_read.cc tests.pyre.lib.memory.map_oob.cc
      tests.pyre.lib.memory.constmap_read.cc tests.pyre.lib.memory.constmap_oob.cc
  )


# timers
pyre_test_driver(tests/pyre.lib/timers/movement_ms.cc)
pyre_test_driver(tests/pyre.lib/timers/movement_reset.cc)
pyre_test_driver(tests/pyre.lib/timers/movement_sanity.cc)
pyre_test_driver(tests/pyre.lib/timers/movement_sec.cc)
pyre_test_driver(tests/pyre.lib/timers/movement_start.cc)
pyre_test_driver(tests/pyre.lib/timers/movement_stop.cc)
pyre_test_driver(tests/pyre.lib/timers/movement_us.cc)
pyre_test_driver(tests/pyre.lib/timers/process_timer_example.cc)
pyre_test_driver(tests/pyre.lib/timers/process_timer_ms.cc)
pyre_test_driver(tests/pyre.lib/timers/process_timer_reset.cc)
pyre_test_driver(tests/pyre.lib/timers/process_timer_sanity.cc)
pyre_test_driver(tests/pyre.lib/timers/process_timer_shared.cc)
pyre_test_driver(tests/pyre.lib/timers/process_timer_start.cc)
pyre_test_driver(tests/pyre.lib/timers/process_timer_stop.cc)
pyre_test_driver(tests/pyre.lib/timers/proxy_sec.cc)
pyre_test_driver(tests/pyre.lib/timers/registrar_contains.cc)
pyre_test_driver(tests/pyre.lib/timers/registrar_iter.cc)
pyre_test_driver(tests/pyre.lib/timers/registrar_lookup.cc)
pyre_test_driver(tests/pyre.lib/timers/registrar_sanity.cc)
pyre_test_driver(tests/pyre.lib/timers/registrar_shared.cc)
pyre_test_driver(tests/pyre.lib/timers/timers_sanity.cc)
pyre_test_driver(tests/pyre.lib/timers/wall_timer_example.cc)
pyre_test_driver(tests/pyre.lib/timers/wall_timer_ms.cc)
pyre_test_driver(tests/pyre.lib/timers/wall_timer_reset.cc)
pyre_test_driver(tests/pyre.lib/timers/wall_timer_sanity.cc)
pyre_test_driver(tests/pyre.lib/timers/wall_timer_shared.cc)
pyre_test_driver(tests/pyre.lib/timers/wall_timer_start.cc)
pyre_test_driver(tests/pyre.lib/timers/wall_timer_stop.cc)


# viz
pyre_test_driver(tests/pyre.lib/viz/amplitude.cc)
pyre_test_driver(tests/pyre.lib/viz/bmp.cc)
pyre_test_driver(tests/pyre.lib/viz/complex.cc)
pyre_test_driver(tests/pyre.lib/viz/decimate.cc)
pyre_test_driver(tests/pyre.lib/viz/domain_coloring.cc)
pyre_test_driver(tests/pyre.lib/viz/hsb.cc)
pyre_test_driver(tests/pyre.lib/viz/hsl.cc)
pyre_test_driver(tests/pyre.lib/viz/logsaw.cc)
pyre_test_driver(tests/pyre.lib/viz/phase.cc)
pyre_test_driver(tests/pyre.lib/viz/polarsaw.cc)

# some tests require cleanup
add_test(NAME tests.pyre.lib.viz.amplitude.cleanup
  COMMAND ${BASH_PROGRAM} -c "rm amplitude.bmp"
  )

add_test(NAME tests.pyre.lib.viz.bmp.cleanup
  COMMAND ${BASH_PROGRAM} -c "rm chip.bmp"
  )

add_test(NAME tests.pyre.lib.viz.complex.cleanup
  COMMAND ${BASH_PROGRAM} -c "rm complex.bmp"
  )

add_test(NAME tests.pyre.lib.viz.decimate.cleanup
  COMMAND ${BASH_PROGRAM} -c "rm decimate.bmp"
  )

add_test(NAME tests.pyre.lib.viz.domain_coloring.cleanup
  COMMAND ${BASH_PROGRAM} -c "rm domain_coloring.bmp"
  )

add_test(NAME tests.pyre.lib.viz.logsaw.cleanup
  COMMAND ${BASH_PROGRAM} -c "rm logsaw.bmp"
  )

add_test(NAME tests.pyre.lib.viz.phase.cleanup
  COMMAND ${BASH_PROGRAM} -c "rm phase.bmp"
  )

add_test(NAME tests.pyre.lib.viz.polarsaw.cleanup
  COMMAND ${BASH_PROGRAM} -c "rm polarsaw.bmp"
  )

# some tests must happen in a specific order
set_property(TEST tests.pyre.lib.viz.amplitude.cleanup PROPERTY
  DEPENDS tests.pyre.lib.viz.amplitude.cc
  )

set_property(TEST tests.pyre.lib.viz.bmp.cleanup PROPERTY
  DEPENDS tests.pyre.lib.viz.bmp.cc
  )

set_property(TEST tests.pyre.lib.viz.complex.cleanup PROPERTY
  DEPENDS tests.pyre.lib.viz.complex.cc
  )

set_property(TEST tests.pyre.lib.viz.decimate.cleanup PROPERTY
  DEPENDS tests.pyre.lib.viz.decimate.cc
  )

set_property(TEST tests.pyre.lib.viz.domain_coloring.cleanup PROPERTY
  DEPENDS tests.pyre.lib.viz.domain_coloring.cc
  )

set_property(TEST tests.pyre.lib.viz.logsaw.cleanup PROPERTY
  DEPENDS tests.pyre.lib.viz.logsaw.cc
  )

set_property(TEST tests.pyre.lib.viz.phase.cleanup PROPERTY
  DEPENDS tests.pyre.lib.viz.phase.cc
  )

set_property(TEST tests.pyre.lib.viz.polarsaw.cleanup PROPERTY
  DEPENDS tests.pyre.lib.viz.polarsaw.cc
  )


# compact packings
if (HAVE_COMPACT_PACKINGS)
set(definitions "HAVE_COMPACT_PACKINGS")
pyre_test_driver_cxx20(tests/pyre.lib/grid/diagonal_visit.cc)
pyre_add_definitions(tests/pyre.lib/grid/diagonal_visit.cc ${definitions})
pyre_test_driver_cxx20(tests/pyre.lib/grid/symmetric_visit.cc)
pyre_add_definitions(tests/pyre.lib/grid/symmetric_visit.cc ${definitions})
pyre_test_driver_cxx20(tests/pyre.lib/grid/symmetric_sanity.cc)
pyre_add_definitions(tests/pyre.lib/grid/symmetric_sanity.cc ${definitions})
endif()


# tensor
if (HAVE_TENSOR)
set(definitions "HAVE_COMPACT_PACKINGS")

pyre_test_driver_cxx20(tests/pyre.lib/tensor/tensor_canonical_arithmetics.cc)
pyre_add_definitions(tests/pyre.lib/tensor/tensor_canonical_arithmetics.cc ${definitions})

pyre_test_driver_cxx20(tests/pyre.lib/tensor/tensor_canonical_basis.cc)
pyre_add_definitions(tests/pyre.lib/tensor/tensor_canonical_basis.cc ${definitions})

pyre_test_driver_cxx20(tests/pyre.lib/tensor/tensor_cayley_hamilton_theorem.cc)
pyre_add_definitions(tests/pyre.lib/tensor/tensor_cayley_hamilton_theorem.cc ${definitions})

pyre_test_driver_cxx20(tests/pyre.lib/tensor/tensor_compact_arithmetics.cc)
pyre_add_definitions(tests/pyre.lib/tensor/tensor_compact_arithmetics.cc ${definitions})

pyre_test_driver_cxx20(tests/pyre.lib/tensor/tensor_eigenvalues.cc)
pyre_add_definitions(tests/pyre.lib/tensor/tensor_eigenvalues.cc ${definitions})

pyre_test_driver_cxx20(tests/pyre.lib/tensor/tensor_eigenvalues_transformation.cc)
pyre_add_definitions(tests/pyre.lib/tensor/tensor_eigenvalues_transformation.cc ${definitions})

pyre_test_driver_cxx20(tests/pyre.lib/tensor/tensor_identities.cc)
pyre_add_definitions(tests/pyre.lib/tensor/tensor_identities.cc ${definitions})

pyre_test_driver_cxx20(tests/pyre.lib/tensor/tensor_inverse.cc)
pyre_add_definitions(tests/pyre.lib/tensor/tensor_inverse.cc ${definitions})

pyre_test_driver_cxx20(tests/pyre.lib/tensor/tensor_iterators.cc)
pyre_add_definitions(tests/pyre.lib/tensor/tensor_iterators.cc ${definitions})

pyre_test_driver_cxx20(tests/pyre.lib/tensor/tensor_literals.cc)
pyre_add_definitions(tests/pyre.lib/tensor/tensor_literals.cc ${definitions})

pyre_test_driver_cxx20(tests/pyre.lib/tensor/tensor_matrix_product.cc)
pyre_add_definitions(tests/pyre.lib/tensor/tensor_matrix_product.cc ${definitions})

pyre_test_driver_cxx20(tests/pyre.lib/tensor/tensor_print.cc)
pyre_add_definitions(tests/pyre.lib/tensor/tensor_print.cc ${definitions})

pyre_test_driver_cxx20(tests/pyre.lib/tensor/tensor_symmetry.cc)
pyre_add_definitions(tests/pyre.lib/tensor/tensor_symmetry.cc ${definitions})

pyre_test_driver_cxx20(tests/pyre.lib/tensor/tensor_transpose.cc)
pyre_add_definitions(tests/pyre.lib/tensor/tensor_transpose.cc ${definitions})

pyre_test_driver_cxx20(tests/pyre.lib/tensor/tensor_utilities.cc)
pyre_add_definitions(tests/pyre.lib/tensor/tensor_utilities.cc ${definitions})

endif()


# end of file
