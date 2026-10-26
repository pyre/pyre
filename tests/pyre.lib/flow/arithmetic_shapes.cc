// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// portability
#include <portinfo>
// STL
#include <cassert>
// support
#include <pyre/journal.h>
#include <pyre/flow.h>


// type aliases
// pick a cell type
using cell_t = double;
// a packing
using packing_t = pyre::grid::canonical_t<2>;
// and a storage strategy
using storage_t = pyre::memory::heap_t<cell_t>;
// use them to make a grid
using grid_t = pyre::grid::grid_t<packing_t, storage_t>;
// the tiles
using tile_t = pyre::flow::products::tile_t<grid_t>;
// and the scalars
using scalar_t = pyre::flow::products::var_t<cell_t>;
// the sum of two tiles
using add_t = pyre::flow::factories::operators::add_t<tile_t>;
// and the product of a tile and a scalar
using scale_t = pyre::flow::factories::operators::multiply_t<tile_t, scalar_t>;

// driver: tiles of different shapes are refused with an exception that python can catch
int
main(int argc, char * argv[])
{
    // the complaints are expected, so keep them quiet
    pyre::journal::error_t::quiet();

    // make two tiles with the same number of cells but different shapes
    auto wide = tile_t::create("wide", tile_t::shape_type(2, 8), 1);
    auto tall = tile_t::create("tall", tile_t::shape_type(8, 2), 2);
    // and a result
    auto sum = tile_t::create("sum", tile_t::shape_type(2, 8), 0);
    // make the operator
    auto add = add_t::create("add");
    // wire it
    add->op1(wide);
    add->op2(tall);
    add->result(sum);
    // attempt to
    try {
        // compute the sum
        sum->read();
        // which should be unreachable
        assert(false);
    }
    // the mismatch is reported
    catch (const pyre::journal::application_error &) {
        // as expected
    }

    // a tile scaled into a result of another shape
    auto scaled = tile_t::create("scaled", tile_t::shape_type(4, 4), 0);
    // by a scalar
    auto factor = scalar_t::create("factor", 2);
    // make the operator
    auto scale = scale_t::create("scale");
    // wire it
    scale->op1(wide);
    scale->op2(factor);
    scale->result(scaled);
    // attempt to
    try {
        // compute the product
        scaled->read();
        // which should be unreachable
        assert(false);
    }
    // the mismatch is reported
    catch (const pyre::journal::application_error &) {
        // as expected
    }

    // all done
    return 0;
}


// end of file
