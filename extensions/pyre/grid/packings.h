// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// the {pyre} extension namespace
namespace pyre::py::grid {
    // the packing instantiations
    void canonical1d(py::module &);
    void canonical2d(py::module &);
    void canonical3d(py::module &);
    void canonical4d(py::module &);

    // the interface decorator
    template <class packingT>
    void packingInterface(py::class_<packingT> &);

} // namespace pyre::py::grid


// end of file
