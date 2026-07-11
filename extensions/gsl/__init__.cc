// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"


// the local helpers
namespace {
    // what gsl does when one of its routines is handed something it cannot use
    //
    // the library aborts the process by default, which is no way to treat an interpreter; so we
    // take the report and hand it to a journal channel instead, and let the routine return its
    // error code to whoever called it
    void errorHandler(const char * reason, const char *, int, int)
    {
        // make a channel
        auto channel = pyre::journal::warning_t("gsl");
        // and complain
        channel
            // the reason
            << "gsl error: "
            << reason
            // flush
            << pyre::journal::endl(__HERE__);
        // all done
        return;
    }
} // namespace


// the module entry point
PYBIND11_MODULE(libgsl, m)
{
    // the docstring
    m.doc() = "the gsl extension module";

    // what the package says about itself
    gsl::py::metadata(m);
    // the blas and eigen flag enumerations, before anybody that takes them by default
    gsl::py::enums(m);

    // the data types gsl allocates and releases
    gsl::py::vector(m);
    gsl::py::matrix(m);
    gsl::py::rng(m);
    gsl::py::permutation(m);
    gsl::py::histogram(m);

    // the free-function modules
    gsl::py::stats(m);
    gsl::py::linalg(m);
    gsl::py::blas(m);
    gsl::py::pdf(m);

    // the mpi partitioning, when the extension was built against mpi
#if defined(WITH_MPI)
    gsl::py::partition(m);
#endif

    // route gsl's complaints into a journal channel, rather than letting the library take the
    // whole process down with it
    gsl_set_error_handler(&errorHandler);

    // all done
    return;
}


// end of file
