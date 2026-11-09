// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// external dependencies, and the aliases that shape this namespace
#include "external.h"


// the {libgsl} extension namespace
namespace gsl::py {
    // what the package says about itself
    void metadata(py::module & m);
    // the blas and eigen flag enumerations
    void enums(py::module & m);

    // register the classes of the data types gsl allocates and releases
    void vectorClass(py::module & m);
    void matrixClass(py::module & m);
    void rngClass(py::module & m);
    void permutationClass(py::module & m);
    void histogramClass(py::module & m);

    // and bind their interfaces
    void vector();
    void matrix();
    void rng(py::module & m);
    void permutation();
    void histogram();

    // the free-function modules
    void stats(py::module & m);
    void linalg(py::module & m);
    void blas(py::module & m);
    void pdf(py::module & m);

    // the mpi partitioning, present only when the extension is built against mpi
#if defined(WITH_MPI)
    void partition(py::module & m);
#endif
} // namespace gsl::py


// end of file
