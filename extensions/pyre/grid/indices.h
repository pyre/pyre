// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// the {pyre} extension namespace
namespace pyre::py::grid {
    // the index instantiations
    void index1d(py::module &);
    void index2d(py::module &);
    void index3d(py::module &);
    void index4d(py::module &);

    // the interface decorator
    template <class indexT>
    void indexInterface(py::class_<indexT> &);

} // namespace pyre::py::grid


// end of file
