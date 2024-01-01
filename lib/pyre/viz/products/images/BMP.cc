// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2024 all rights reserved

// externals
#include "../external.h"
// forward declarations
#include "../forward.h"
// type aliases
#include "../api.h"

// my class declaration
#include "BMP.h"

// destructor
pyre::viz::products::images::BMP::~BMP()
{
    // free my buffer
    delete[] _data;

    // make a channel
    auto channel = pyre::journal::debug_t("pyre.viz.products.images.bmp");
    // let me know
    channel
        // mark
        << "bmp at " << this << ": destroy"
        << pyre::journal::newline
        // flush
        << pyre::journal::endl(__HERE__);

    // all done
    return;
}

// internals
auto
pyre::viz::products::images::BMP::dump() -> ref_type
{
    // build a reference
    auto self = std::dynamic_pointer_cast<BMP>(ref());
    // unpack my shape
    auto [width, height] = _shape;
    // and build a view over my buffer
    auto view = read();
    // make a channel
    auto channel = pyre::journal::debug_t("pyre.viz.products.images.bmp");
    // show me
    channel
        // the product
        << "bmp " << this
        << pyre::journal::newline
        // indent
        << pyre::journal::indent
        // its shape
        << "shape: " << width << " x " << height
        << pyre::journal::newline
        // its size
        << "cells: " << view.cells()
        << pyre::journal::newline
        // its data buffer location
        << "data: " << view.where()
        << pyre::journal::newline
        // outdent
        << pyre::journal::outdent
        // flush
        << pyre::journal::endl(__HERE__);

    // all done
    return self;
}

// end of file