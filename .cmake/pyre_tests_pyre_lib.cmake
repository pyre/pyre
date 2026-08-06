# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


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
pyre_test_driver(tests/pyre.lib/grid/canonical_isomorphism.cc)
pyre_test_driver(tests/pyre.lib/grid/canonical_isomorphism_origin.cc)
pyre_test_driver(tests/pyre.lib/grid/canonical_nudge.cc)
pyre_test_driver(tests/pyre.lib/grid/canonical_offset.cc)
pyre_test_driver(tests/pyre.lib/grid/canonical_sanity.cc)
pyre_test_driver(tests/pyre.lib/grid/canonical_slice.cc)
pyre_test_driver(tests/pyre.lib/grid/canonical_visit_order.cc)
pyre_test_driver(tests/pyre.lib/grid/chunked_injective.cc)
pyre_test_driver(tests/pyre.lib/grid/chunked_offset.cc)
pyre_test_driver(tests/pyre.lib/grid/chunked_sanity.cc)
pyre_test_driver(tests/pyre.lib/grid/chunked_tiles.cc)
pyre_test_driver(tests/pyre.lib/grid/concepts.cc)
pyre_test_driver(tests/pyre.lib/grid/diagonal_sink.cc)
pyre_test_driver(tests/pyre.lib/grid/dynamic_chunked_sanity.cc)
pyre_test_driver(tests/pyre.lib/grid/dynamic_chunked_tiles.cc)
pyre_test_driver(tests/pyre.lib/grid/dynamic_mosaic_pane.cc)
pyre_test_driver(tests/pyre.lib/grid/grid_heap_access.cc)
pyre_test_driver(tests/pyre.lib/grid/grid_heap_box.cc)
pyre_test_driver(tests/pyre.lib/grid/grid_heap_chunked.cc)
pyre_test_driver(tests/pyre.lib/grid/grid_heap_iteration.cc)
pyre_test_driver(tests/pyre.lib/grid/grid_heap_slice.cc)
pyre_test_driver(tests/pyre.lib/grid/grid_map_access.cc)
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
pyre_test_driver(tests/pyre.lib/grid/mosaic_access.cc)
pyre_test_driver(tests/pyre.lib/grid/mosaic_pane.cc)
pyre_test_driver(tests/pyre.lib/grid/mosaic_release.cc)
pyre_test_driver(tests/pyre.lib/grid/mosaic_window.cc)
pyre_test_driver(tests/pyre.lib/grid/order_access.cc)
pyre_test_driver(tests/pyre.lib/grid/order_c.cc)
pyre_test_driver(tests/pyre.lib/grid/order_fortran.cc)
pyre_test_driver(tests/pyre.lib/grid/order_sanity.cc)
pyre_test_driver(tests/pyre.lib/grid/sanity.cc)
pyre_test_driver(tests/pyre.lib/grid/shape_access.cc)
pyre_test_driver(tests/pyre.lib/grid/shape_arithmetic.cc)
pyre_test_driver(tests/pyre.lib/grid/shape_cartesian.cc)
pyre_test_driver(tests/pyre.lib/grid/shape_fill.cc)
pyre_test_driver(tests/pyre.lib/grid/shape_sanity.cc)
pyre_test_driver(tests/pyre.lib/grid/shape_scaling.cc)
pyre_test_driver(tests/pyre.lib/grid/shape_structured_binding.cc)
pyre_test_driver(tests/pyre.lib/grid/shape_zero.cc)
pyre_test_driver(tests/pyre.lib/grid/symmetric_sharing.cc)



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
pyre_test_driver(tests/pyre.lib/memory/paged_access.cc)
pyre_test_driver(tests/pyre.lib/memory/paged_oob.cc)
pyre_test_driver(tests/pyre.lib/memory/paged_poison.cc)
pyre_test_driver(tests/pyre.lib/memory/paged_release.cc)
pyre_test_driver(tests/pyre.lib/memory/paged_sanity.cc)
pyre_test_driver(tests/pyre.lib/memory/paged_state.cc)
pyre_test_driver(tests/pyre.lib/memory/view_access.cc)
pyre_test_driver(tests/pyre.lib/memory/view_oob.cc)
pyre_test_driver(tests/pyre.lib/memory/stack_access.cc)
pyre_test_driver(tests/pyre.lib/memory/heap_slice.cc)
pyre_test_driver(tests/pyre.lib/memory/constheap_slice.cc)
pyre_test_driver(tests/pyre.lib/memory/view_slice.cc)
pyre_test_driver(tests/pyre.lib/memory/constview_slice.cc)
pyre_test_driver(tests/pyre.lib/memory/map_slice.cc)
pyre_test_driver(tests/pyre.lib/memory/constmap_slice.cc)

# some tests must happen in a specific order
set_property(TEST tests.pyre.lib.memory.filemap_write.cc PROPERTY
  DEPENDS tests.pyre.lib.memory.filemap_create.cc
  )
set_property(TEST tests.pyre.lib.memory.filemap_read.cc PROPERTY
  DEPENDS tests.pyre.lib.memory.filemap_write.cc
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

# the drivers leave their scratch products behind so they can be inspected; sweep them
# {filemap.dat} is built up by a chain of drivers, so the sweep waits for every link
pyre_test_driver_cleanup(filemap.dat
  tests/pyre.lib/memory/filemap_create.cc
  tests/pyre.lib/memory/filemap_write.cc
  tests/pyre.lib/memory/filemap_read.cc
  )
# {map.dat} is shared by a fan of consumers, so the sweep waits for all of them
pyre_test_driver_cleanup(map.dat
  tests/pyre.lib/memory/map_create.cc
  tests/pyre.lib/memory/map_write.cc
  tests/pyre.lib/memory/map_read.cc
  tests/pyre.lib/memory/map_oob.cc
  tests/pyre.lib/memory/constmap_read.cc
  tests/pyre.lib/memory/constmap_oob.cc
  )
# the slice tests each own their file
pyre_test_driver_cleanup(map_slice.dat tests/pyre.lib/memory/map_slice.cc)
pyre_test_driver_cleanup(constmap_slice.dat tests/pyre.lib/memory/constmap_slice.cc)


# typelists
pyre_test_driver(tests/pyre.lib/typelists/append.cc)
pyre_test_driver(tests/pyre.lib/typelists/apply.cc)
pyre_test_driver(tests/pyre.lib/typelists/cartesian.cc)
pyre_test_driver(tests/pyre.lib/typelists/concat.cc)
pyre_test_driver(tests/pyre.lib/typelists/grid.cc)
pyre_test_driver(tests/pyre.lib/typelists/lift.cc)
pyre_test_driver(tests/pyre.lib/typelists/merge.cc)
pyre_test_driver(tests/pyre.lib/typelists/prepend.cc)
pyre_test_driver(tests/pyre.lib/typelists/typelist.cc)


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


# flow
pyre_test_driver(tests/pyre.lib/flow/add_tiles.cc)
pyre_test_driver(tests/pyre.lib/flow/add_variables.cc)
pyre_test_driver(tests/pyre.lib/flow/calc_tiles.cc)
pyre_test_driver(tests/pyre.lib/flow/calc_variables.cc)
pyre_test_driver(tests/pyre.lib/flow/flow.cc)
pyre_test_driver(tests/pyre.lib/flow/multiply_tiles.cc)
pyre_test_driver(tests/pyre.lib/flow/multiply_variables.cc)


# viz
pyre_test_driver(tests/pyre.lib/viz/iterators/amplitude.cc)
pyre_test_driver(tests/pyre.lib/viz/flow/affine.cc)
pyre_test_driver(tests/pyre.lib/viz/flow/amplitude.cc)
pyre_test_driver(tests/pyre.lib/viz/flow/bmp.cc)
pyre_test_driver(tests/pyre.lib/viz/flow/complex.cc)
pyre_test_driver(tests/pyre.lib/viz/flow/constant.cc)
pyre_test_driver(tests/pyre.lib/viz/flow/cycle.cc)
pyre_test_driver(tests/pyre.lib/viz/flow/decimate.cc)
pyre_test_driver(tests/pyre.lib/viz/flow/geometric.cc)
pyre_test_driver(tests/pyre.lib/viz/flow/gray.cc)
pyre_test_driver(tests/pyre.lib/viz/flow/hl.cc)
pyre_test_driver(tests/pyre.lib/viz/flow/hsb.cc)
pyre_test_driver(tests/pyre.lib/viz/flow/hsl.cc)
pyre_test_driver(tests/pyre.lib/viz/flow/imaginary.cc)
pyre_test_driver(tests/pyre.lib/viz/flow/logsaw.cc)
pyre_test_driver(tests/pyre.lib/viz/flow/parametric.cc)
pyre_test_driver(tests/pyre.lib/viz/flow/phase.cc)
pyre_test_driver(tests/pyre.lib/viz/flow/polarsaw.cc)
pyre_test_driver(tests/pyre.lib/viz/flow/power.cc)
pyre_test_driver(tests/pyre.lib/viz/flow/real.cc)
pyre_test_driver(tests/pyre.lib/viz/flow/uniform.cc)
pyre_test_driver(tests/pyre.lib/viz/iterators/bmp.cc)
pyre_test_driver(tests/pyre.lib/viz/iterators/complex.cc)
pyre_test_driver(tests/pyre.lib/viz/iterators/decimate.cc)
pyre_test_driver(tests/pyre.lib/viz/iterators/domain_coloring.cc)
pyre_test_driver(tests/pyre.lib/viz/iterators/logsaw.cc)
pyre_test_driver(tests/pyre.lib/viz/iterators/phase.cc)
pyre_test_driver(tests/pyre.lib/viz/iterators/polarsaw.cc)

# the drivers leave their scratch products behind so they can be inspected; sweep them
pyre_test_driver_cleanup(pyre_viz_flow_amplitude.bmp tests/pyre.lib/viz/flow/amplitude.cc)
pyre_test_driver_cleanup(pyre_viz_flow_bmp.bmp tests/pyre.lib/viz/flow/bmp.cc)
pyre_test_driver_cleanup(pyre_viz_flow_complex.bmp tests/pyre.lib/viz/flow/complex.cc)
pyre_test_driver_cleanup(pyre_viz_flow_decimate.bmp tests/pyre.lib/viz/flow/decimate.cc)
pyre_test_driver_cleanup(pyre_viz_flow_gray.bmp tests/pyre.lib/viz/flow/gray.cc)
pyre_test_driver_cleanup(pyre_viz_flow_hl.bmp tests/pyre.lib/viz/flow/hl.cc)
pyre_test_driver_cleanup(pyre_viz_flow_hsb.bmp tests/pyre.lib/viz/flow/hsb.cc)
pyre_test_driver_cleanup(pyre_viz_flow_hsl.bmp tests/pyre.lib/viz/flow/hsl.cc)
pyre_test_driver_cleanup(pyre_viz_flow_imaginary.bmp tests/pyre.lib/viz/flow/imaginary.cc)
pyre_test_driver_cleanup(pyre_viz_flow_phase.bmp tests/pyre.lib/viz/flow/phase.cc)
pyre_test_driver_cleanup(pyre_viz_flow_real.bmp tests/pyre.lib/viz/flow/real.cc)
pyre_test_driver_cleanup(pyre_viz_iterators_amplitude.bmp tests/pyre.lib/viz/iterators/amplitude.cc)
pyre_test_driver_cleanup(pyre_viz_iterators_bmp.bmp tests/pyre.lib/viz/iterators/bmp.cc)
pyre_test_driver_cleanup(pyre_viz_iterators_complex.bmp tests/pyre.lib/viz/iterators/complex.cc)
pyre_test_driver_cleanup(pyre_viz_iterators_decimate.bmp tests/pyre.lib/viz/iterators/decimate.cc)
pyre_test_driver_cleanup(pyre_viz_iterators_domain_coloring.bmp tests/pyre.lib/viz/iterators/domain_coloring.cc)
pyre_test_driver_cleanup(pyre_viz_iterators_logsaw.bmp tests/pyre.lib/viz/iterators/logsaw.cc)
pyre_test_driver_cleanup(pyre_viz_iterators_phase.bmp tests/pyre.lib/viz/iterators/phase.cc)
pyre_test_driver_cleanup(pyre_viz_iterators_polarsaw.bmp tests/pyre.lib/viz/iterators/polarsaw.cc)


# math
pyre_test_driver(tests/pyre.lib/math/transcendental.cc)


# tensor

pyre_test_driver(tests/pyre.lib/tensor/tensor_concepts.cc)

pyre_test_driver(tests/pyre.lib/tensor/tensor_contractions.cc)

pyre_test_driver(tests/pyre.lib/tensor/tensor_canonical_arithmetics.cc)

pyre_test_driver(tests/pyre.lib/tensor/tensor_canonical_basis.cc)

pyre_test_driver(tests/pyre.lib/tensor/tensor_cayley_hamilton_theorem.cc)

pyre_test_driver(tests/pyre.lib/tensor/tensor_compact_arithmetics.cc)

pyre_test_driver(tests/pyre.lib/tensor/tensor_dot.cc)

pyre_test_driver(tests/pyre.lib/tensor/tensor_dyadic.cc)

pyre_test_driver(tests/pyre.lib/tensor/tensor_eigenvalues.cc)

pyre_test_driver(tests/pyre.lib/tensor/tensor_eigenvalues_transformation.cc)

pyre_test_driver(tests/pyre.lib/tensor/tensor_identities.cc)

pyre_test_driver(tests/pyre.lib/tensor/tensor_diagonal_inverse.cc)

pyre_test_driver(tests/pyre.lib/tensor/tensor_linear_system.cc)

pyre_test_driver(tests/pyre.lib/tensor/tensor_iterators.cc)

pyre_test_driver(tests/pyre.lib/tensor/tensor_literals.cc)

pyre_test_driver(tests/pyre.lib/tensor/tensor_matrix_build.cc)

pyre_test_driver(tests/pyre.lib/tensor/tensor_matrix_assignment.cc)

pyre_test_driver(tests/pyre.lib/tensor/tensor_matrix_equal.cc)

pyre_test_driver(tests/pyre.lib/tensor/tensor_matrix_norm.cc)

pyre_test_driver(tests/pyre.lib/tensor/tensor_matrix_product.cc)

pyre_test_driver(tests/pyre.lib/tensor/tensor_matrix_vector_product.cc)

pyre_test_driver(tests/pyre.lib/tensor/tensor_fourth_order_contraction.cc)

pyre_test_driver(tests/pyre.lib/tensor/tensor_print.cc)

pyre_test_driver(tests/pyre.lib/tensor/tensor_symmetry.cc)

pyre_test_driver(tests/pyre.lib/tensor/tensor_transpose.cc)

pyre_test_driver(tests/pyre.lib/tensor/tensor_utilities.cc)

pyre_test_driver(tests/pyre.lib/tensor/quaternion_composition.cc)

pyre_test_driver(tests/pyre.lib/tensor/quaternion_from_rotation_matrix.cc)

pyre_test_driver(tests/pyre.lib/tensor/quaternion_inverse.cc)


# end of file
