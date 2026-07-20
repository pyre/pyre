// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// support
#include <cassert>
// get the grid
#include <pyre/_grid_.h>
// and the storage strategies
#include <pyre/memory.h>


// the parts of the grid under test
using canonical_t = pyre::grid::canonical_t<3>;
using heap_t = pyre::memory::heap_t<pyre::memory::float64_t>;
using grid_t = pyre::grid::grid_t<canonical_t, heap_t>;
// and the pieces used to address it
using shape_t = canonical_t::shape_type;
using index_t = canonical_t::index_type;
// the hyperplane that survives pinning one axis is a grid of lower rank
using plane_index_t = pyre::grid::index_t<2>;


// verify that a hyperplane addresses the cells of the grid it was cut from
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("grid_heap_slice");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.grid");

    // pick a shape
    constexpr shape_t shape { 2, 3, 4 };
    // lay it out canonically over enough cells to hold it
    const canonical_t packing { shape };
    // put the cells on the heap
    const heap_t store { packing.cells() };
    // and make a grid
    const grid_t grid { packing, store };

    // stamp every cell with its own offset, so a cell reached two ways is recognizable
    for (auto it = grid.packing().begin(); it != grid.packing().end(); ++it) {
        // each cell remembers where it lives
        grid[*it] = static_cast<grid_t::value_type>(packing.offset(*it));
    }

    // cut the plane that keeps axes 0 and 2, pinning axis 1 at 1
    const auto plane = grid.slice<0, 2>(index_t { 0, 1, 0 });
    // the survivors keep their extents, in the order they were named
    assert((plane.packing().shape() == pyre::grid::shape_t<2> { 2, 4 }));

    // every cell of the plane must be a cell of the parent
    for (canonical_t::index_type::value_type i = 0; i < 2; ++i) {
        // sweep the second surviving axis too
        for (canonical_t::index_type::value_type k = 0; k < 4; ++k) {
            // name the cell in the plane's own index space
            auto flat = plane_index_t { i, k };
            // and the same cell in the parent's, with the pinned axis put back
            auto full = index_t { i, 1, k };
            // show me
            channel << pyre::journal::at() << "  " << flat << " -> " << plane[flat] << " vs "
                    << full << " -> " << grid[full] << pyre::journal::newline;
            // the two routes must arrive at the same cell
            assert((plane[flat] == grid[full]));
        }
    }

    // writing through the plane must be visible in the parent
    plane[plane_index_t { 1, 3 }] = -11;
    // so ask the parent for the cell that names the same place
    assert((grid[index_t { 1, 1, 3 }] == -11));

    // flush the trace
    channel << pyre::journal::endl;

    // all done
    return 0;
}


// end of file
