// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

#if !defined(gsl_extension_api_h)
#define gsl_extension_api_h

// forward declarations
#include "forward.h"

// pybind11
#include <pybind11/pybind11.h>

// GSL raw types (needed for return types below)
#include <gsl/gsl_histogram.h>
#include <gsl/gsl_matrix.h>
#include <gsl/gsl_permutation.h>
#include <gsl/gsl_rng.h>
#include <gsl/gsl_vector.h>

// pointer extraction helpers: retrieve the raw GSL pointer from a Python-wrapped object
namespace pyre::gsl {

    inline gsl_vector * get_vector(pybind11::handle obj) {
        return pybind11::cast<Vector &>(obj).ptr;
    }

    inline gsl_matrix * get_matrix(pybind11::handle obj) {
        return pybind11::cast<Matrix &>(obj).ptr;
    }

    inline gsl_rng * get_rng(pybind11::handle obj) {
        return pybind11::cast<RNG &>(obj).ptr;
    }

    inline gsl_permutation * get_permutation(pybind11::handle obj) {
        return pybind11::cast<Permutation &>(obj).ptr;
    }

    inline gsl_histogram * get_histogram(pybind11::handle obj) {
        return pybind11::cast<Histogram &>(obj).ptr;
    }

} // namespace pyre::gsl

#endif

// end of file
