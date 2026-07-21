// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// get the grid
#include <pyre/grid.h>
// and the storage strategies a grid is built over
#include <pyre/memory.h>


// the layouts under test
using canonical_t = pyre::grid::canonical_t<3>;
using diagonal_t = pyre::grid::diagonal_t<3>;
using symmetric_t = pyre::grid::symmetric_t<3>;
using dynamic_t = pyre::grid::dynamic_canonical_t;
// and a representative storage strategy
using heap_t = pyre::memory::heap_t<pyre::memory::float64_t>;

// pull in the vocabulary
namespace concepts = pyre::grid::concepts;


// verify that the layouts and storage strategies satisfy the contracts they claim
int
main()
{
    // a compile time layout knows how to address a grid
    static_assert(concepts::PackingStrategy<canonical_t>);
    // its offset map is injective, so it can be run backwards
    static_assert(concepts::InvertiblePacking<canonical_t>);
    // and it addresses memory by a fixed increment per axis
    static_assert(concepts::StridedPacking<canonical_t>);
    // it packs no tiles, so it makes no promises about them
    static_assert(!concepts::TiledPacking<canonical_t>);

    // a diagonal layout is a packing strategy too, but a sparse one
    static_assert(concepts::PackingStrategy<diagonal_t>);
    // it stores no per-axis stride vector, so it does not address memory by strides
    static_assert(!concepts::StridedPacking<diagonal_t>);
    // and it packs no tiles
    static_assert(!concepts::TiledPacking<diagonal_t>);

    // a symmetric layout is likewise a sparse packing strategy
    static_assert(concepts::PackingStrategy<symmetric_t>);
    // with no strides and no tiles of its own
    static_assert(!concepts::StridedPacking<symmetric_t>);
    static_assert(!concepts::TiledPacking<symmetric_t>);

    // a runtime rank layout addresses a grid the same way
    static_assert(concepts::PackingStrategy<dynamic_t>);
    // and offers the same guarantees, since it is the same isomorphism
    static_assert(concepts::InvertiblePacking<dynamic_t>);
    static_assert(concepts::StridedPacking<dynamic_t>);
    static_assert(!concepts::TiledPacking<dynamic_t>);

    // a heap names and reaches its cells
    static_assert(concepts::StorageStrategy<heap_t>);
    // and keeps them in one expanse, so it can hand out their address
    static_assert(concepts::ContiguousStorage<heap_t>);

    // the packing contract is the only one a grid insists on, so that layouts which store
    // neither strides nor an inverse can still be composed into one
    using grid_t = pyre::grid::grid_t<canonical_t, heap_t>;
    // and a grid over a layout that meets it is a complete type
    static_assert(sizeof(grid_t) > 0);

    // all done
    return 0;
}


// end of file
