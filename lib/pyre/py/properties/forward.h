// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// externals
#include "externals.h"


// the accessors of the properties of bound classes, built so that their signatures name their
// parameters
namespace pyre::py {
    // the setter of a property made from a method of the class bound by {cls}
    template <class classT, class returnT, class ownerT, class argT, bool except>
    inline auto setter(const classT & cls, returnT (ownerT::*method)(argT) noexcept(except))
        -> py::cpp_function;

    // the setter of a property made from a callable that takes an instance of the class bound by
    // {cls} and the new value
    template <class classT, class callableT>
    inline auto setter(const classT & cls, callableT callable) -> py::cpp_function;

    // the getter of a property made from a data member of the class bound by {cls}
    template <class classT, class ownerT, class fieldT>
        requires(!std::is_function_v<fieldT>)
    inline auto getter(const classT & cls, fieldT ownerT::* field) -> py::cpp_function;

    // and its setter
    template <class classT, class ownerT, class fieldT>
        requires(!std::is_function_v<fieldT>)
    inline auto setter(const classT & cls, fieldT ownerT::* field) -> py::cpp_function;
} // namespace pyre::py


// end of file
