// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// get the common ones
#include "../external.h"
// the flow bindings, whose protocols and catalog the viz nodes join
#include "../flow/external.h"
#include "../flow/forward.h"
// get the pyre parts
#include <pyre/viz.h>


// aliases
namespace pyre::py::viz {
    // bitmaps
    using bmp_t = pyre::viz::iterators::codecs::bmp_t;
    // the bitmap image products
    using image_t = pyre::viz::products::images::bmp_t;

} // namespace pyre::py::viz


// end of file
