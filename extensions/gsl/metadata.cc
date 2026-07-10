// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"


// the version number
#define GSL_VERSION "1.0"


// what the package says about itself
void
gsl::py::metadata(py::module & m)
{
    // the copyright note
    m.def(
        // the name
        "copyright",
        // the implementation
        []() -> std::string { return "gsl: (c) 1998-2026 orthologue"; },
        // the docstring
        "the module copyright string");

    // the version
    m.def(
        // the name
        "version",
        // the implementation
        []() -> std::string { return GSL_VERSION; },
        // the docstring
        "the module version string");

    // the license
    m.def(
        // the name
        "license",
        // the implementation
        []() -> std::string {
            return "\n"
                   "    gsl " GSL_VERSION
                   "\n"
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
        },
        // the docstring
        "the module license string");

    // all done
    return;
}


// end of file
