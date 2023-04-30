// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


#include <iostream>
// support
#include <cassert>
// get the grid
#include <pyre/grid.h>


// verify the layout of a grid on the stack
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("grid_stack_sanity");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.stack");

    //  the space dimension
    const int dim = 4;
    // my cell
    using cell_t = double;
    // we'll work with a 2d conventionally packed grid
    using pack_t = pyre::grid::canonical_t<2>;
    // of doubles on the stack
    using storage_t = pyre::memory::stack_t<dim * dim, cell_t>;
    // putting it all together
    using matrix_t = pyre::grid::grid_t<pack_t, storage_t>;

    // shape
    pack_t::shape_type shape { dim, dim };
    // packing
    pack_t layout { shape };
    // instantiate the grid
    matrix_t base { layout };

    // we want to fill each quadrant with different values, so let's start by defining "quadrant"
    auto quad = shape / 2;    // <- this is {dim/2, dim/2}

    // go through the four quadrants
    for (auto t = 0; t < 2; ++t) {
        for (auto b = 0; b < 2; ++b) {
            // describe the restricted index range
            auto box = layout.box({ t * dim / 2, b * dim / 2 }, quad);
            // loop over it
            for (auto idx : box) {
                // and set the value
                // base[idx] = 2*t + b + 1;
                base[idx] = layout[idx] + 1;    // add some spice
            }
        }
    }

    // show me {base}
    channel << "base:" << pyre::journal::newline;
    for (int i = 0; i < shape[0]; ++i) {
        for (int j = 0; j < shape[1]; ++j) {
            channel << "  " << std::setw(2) << base[{ i, j }];
        }
        channel << pyre::journal::newline;
    }
    channel << pyre::journal::endl;

    // pick a magnification factor
    const int ovs = 3;
    // the expanded array shape
    using expstorage_t = pyre::memory::stack_t<ovs * dim * ovs * dim, double>;
    // it is also packed in column major order with origin at {0,0}
    using expmatrix_t = pyre::grid::grid_t<pack_t, expstorage_t>;
    // shape
    pack_t::shape_type expshape { ovs * dim, ovs * dim };
    // packing
    pack_t explayout { expshape };
    // instantiate
    expmatrix_t expanded { explayout };

    // zero it out
    for (auto & cell : expanded) {
        cell = 0;
    }

    // go through the four quadrants
    for (auto t = 0; t < 2; ++t) {
        for (auto b = 0; b < 2; ++b) {
            // the source
            matrix_t::index_type src { t * dim / 2, b * dim / 2 };
            // the shift to the destination
            matrix_t::index_type shift { t * dim * (ovs - 1), b * dim * (ovs - 1) };
            // copy
            for (auto idx : layout.box(src, quad)) {
                expanded[idx + shift] = base[idx];
            }
        }
    }

    // show me {expanded}
    channel << "expanded:" << pyre::journal::newline;
    for (int i = 0; i < expshape[0]; ++i) {
        for (int j = 0; j < expshape[1]; ++j) {
            channel << "  " << std::setw(2) << expanded[{ i, j }];
        }
        channel << pyre::journal::newline;
    }
    channel << pyre::journal::endl;

    // all done
    return 0;
}


// end of file
