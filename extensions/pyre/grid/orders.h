// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// the {pyre} extension namespace
namespace pyre::py::grid {
    // the order instantiations
    void order1d(py::module &);
    void order2d(py::module &);
    void order3d(py::module &);
    void order4d(py::module &);

    // the interface decorator
    template <class orderT>
    void orderInterface(py::class_<orderT> &);

} // namespace pyre::py::grid


// end of file
