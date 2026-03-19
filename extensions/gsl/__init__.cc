// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// externals
#include "external.h"
// subsystem binders
#include "forward.h"


// GSL error handler: route errors through the pyre journal
static void
errorHandler(const char * reason, const char *, int, int)
{
    // make a channel
    auto channel = pyre::journal::warning_t("gsl");
    // report
    channel << "GSL error: " << reason << pyre::journal::endl(__HERE__);
}


// the module entry point
PYBIND11_MODULE(gsl, m)
{
    // documentation
    m.doc() = "pyre gsl extension module";

    // install the GSL error handler
    gsl_set_error_handler(&errorHandler);
    // initialize the table of known random number generators
    pyre::gsl::py::rng_initialize();

    // bind types and functions in dependency order:
    // register each class before it is used as an argument/return type
    pyre::gsl::py::vector(m);      // registers Vector, VectorView
    pyre::gsl::py::matrix(m);      // registers Matrix, MatrixView
    pyre::gsl::py::rng(m);         // registers RNG
    pyre::gsl::py::permutation(m); // registers Permutation
    pyre::gsl::py::histogram(m);   // registers Histogram
    // functions only (types already registered above)
    pyre::gsl::py::blas(m);
    pyre::gsl::py::linalg(m);
    pyre::gsl::py::pdf(m);
    pyre::gsl::py::stats(m);

#if defined(WITH_MPI)
    pyre::gsl::py::partition(m);
#endif
}


// end of file
