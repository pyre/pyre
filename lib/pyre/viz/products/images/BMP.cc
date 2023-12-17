// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// externals
#include "../../public.h"
// forward declarations
#include "../../forward.h"
// type aliases
#include "../../api.h"

// my class declaration
#include "BMP.h"

// destructor
pyre::viz::products::images::BMP::~BMP()
{
    // free my buffer
    delete[] _data;

    // make a channel
    auto channel = pyre::journal::debug_t("pyre.viz.products.bmp");
    // let me know
    channel
        // mark
        << "bmp: destroying bitmap at "
        << (void *) this
        // flush
        << pyre::journal::endl(__HERE__);

    // all done
    return;
}

// internals
auto
pyre::viz::products::images::BMP::flush() -> void
{
    // chain up
    pyre::flow::product_t::flush();
    // invalidate my memory buffer
    delete[] _data;
    // all done
    return;
}

auto
pyre::viz::products::images::BMP::dump() -> ref_type
{
    // build a reference
    auto self = std::dynamic_pointer_cast<BMP>(ref());
    // unpack my shape
    auto [width, height] = _shape;
    // and build a view over my buffer
    auto view = data();
    // make a channel
    auto channel = pyre::journal::debug_t("pyre.viz.products.bmp");
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