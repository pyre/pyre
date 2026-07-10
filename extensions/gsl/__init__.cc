// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"
// the entities that have not moved to pybind11 yet
#include "legacy.h"
// the random number generators, whose table has to be built before anybody asks for one
#include "rng.h"


// the local helpers
namespace {
    // what gsl does when one of its routines is handed something it cannot use
    //
    // the library aborts the process by default, which is no way to treat an interpreter; so we
    // take the report and hand it to a journal channel instead, and let the routine return its
    // error code to whoever called it
    void
    errorHandler(const char * reason, const char *, int, int)
    {
        // make a channel
        auto channel = pyre::journal::warning_t("gsl");
        // and complain
        channel
            // the reason
            << "gsl error: " << reason
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

    // graft on the entities that are still spelled as free functions over capsules; the table
    // shrinks with every class that moves to pybind11, and this call goes away with the last one
    if (PyModule_AddFunctions(m.ptr(), gsl::legacy::methods) < 0) {
        // if the graft failed, the module is not usable, and python already knows why
        throw pybind11::error_already_set();
    }

    // route gsl's complaints into a journal channel, rather than letting the library take the
    // whole process down with it
    gsl_set_error_handler(&errorHandler);
    // build the table of known random number generators
    gsl::rng::initialize();

    // all done
    return;
}


// end of file
