// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// externals
#include "externals.h"
// forward declarations
#include "forward.h"


// a radar sample crosses into python as the tuple of its two counts, {(i, q)}, and comes back
// from any sequence of two integers; counts stored in another byte order reach python as their
// values
template <typename T>
class pybind11::detail::type_caster<pyre::memory::IQ<T>> {
    // types
public:
    // the sample
    using sample_type = pyre::memory::IQ<T>;
    // its counts, in the host's order
    using count_type = pyre::memory::native_t<T>;

    // my value and the generic cast entry points; the stubs show a pair of integers
    PYBIND11_TYPE_CASTER(sample_type, const_name("tuple[int, int]"));

    // interface
public:
    // fill my value from a python {source}
    auto load(handle source, bool convert) -> bool;
    // build the python face of a {sample}
    static auto cast(const sample_type & sample, return_value_policy policy, handle parent)
        -> handle;
};


// get the inline definitions
#include "IQ.icc"


// end of file
