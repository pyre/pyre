// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// support
#include <cassert>
// get the grid
#include <pyre/grid.h>


// a matrix is a rank-2 grid on the heap, packed in column major order
using matrix_t = pyre::grid::grid_t<pyre::grid::canonical_t<2>, pyre::memory::heap_t<double>>;


// example from the spectral expansion step of {ampcor}
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("grid_heap_expand");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.heap");

    // pick a dimension for the base array
    const auto dim = 4;
    // our base array is {dim x dim}
    matrix_t::shape_type shape { dim, dim };
    // it is packed in column major order with origin at {0,0}
    matrix_t::packing_type layout { shape };
    // make the base matrix
    matrix_t base { layout, layout.cells() };

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
    auto ovs = 3;
    // the expanded array shape
    auto expandedShape = ovs * shape;
    // it is also packed in column major order with origin at {0,0}
    matrix_t::packing_type expandedLayout { expandedShape };
    // instantiate
    matrix_t expanded { expandedLayout, expandedLayout.cells() };
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
    for (int i = 0; i < expandedShape[0]; ++i) {
        for (int j = 0; j < expandedShape[1]; ++j) {
            channel << "  " << std::setw(2) << expanded[{ i, j }];
        }
        channel << pyre::journal::newline;
    }
    channel << pyre::journal::endl;

    // all done
    return 0;
}


// end of file
