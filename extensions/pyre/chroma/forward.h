// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

#pragma once


// the {chroma} binding namespace
namespace pyre::py::chroma {
    // bind the color type
    void color(py::module &);
    // bind the {rgb} converters and the color palette
    void rgb(py::module &);
    // bind the {ansi} serializers
    void ansi(py::module &);
} // namespace pyre::py::chroma


// end of file
