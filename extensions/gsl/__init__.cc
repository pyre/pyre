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
    // metadata
    m.attr("version")   = "1.0";
    m.attr("copyright") = "gsl: (c) 1998-2026 orthologue";
    m.attr("license")   =
        "\n"
        "    gsl 1.0\n"
        "    Copyright (c) 1998-2026 orthologue\n"
        "    All Rights Reserved\n"
        "\n"
        "    Redistribution and use in source and binary forms, with or without\n"
        "    modification, are permitted provided that the following conditions\n"
        "    are met:\n"
        "\n"
        "    * Redistributions of source code must retain the above copyright\n"
        "      notice, this list of conditions and the following disclaimer.\n"
        "\n"
        "    * Redistributions in binary form must reproduce the above copyright\n"
        "      notice, this list of conditions and the following disclaimer in\n"
        "      the documentation and/or other materials provided with the\n"
        "      distribution.\n"
        "\n"
        "    * Neither the name \"gsl\" nor the names of its contributors may be\n"
        "      used to endorse or promote products derived from this software\n"
        "      without specific prior written permission.\n"
        "\n"
        "    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS\n"
        "    \"AS IS\" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT\n"
        "    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS\n"
        "    FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE\n"
        "    COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,\n"
        "    INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,\n"
        "    BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;\n"
        "    LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER\n"
        "    CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT\n"
        "    LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN\n"
        "    ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE\n"
        "    POSSIBILITY OF SUCH DAMAGE.\n";

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
