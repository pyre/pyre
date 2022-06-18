// -*- C++ -*-
//
// {project.authors}
// (c) {project.span} all rights reserved


// external
#include "external.h"
// namespace setup
#include "forward.h"


// the module entry point
PYBIND11_MODULE({project.name}, m)
{{
    // the doc string
    m.doc() = "the lib{project.name} bindings";

    // bind the opaque types
    {project.name}::py::opaque(m);
    // register the exception types
    {project.name}::py::exceptions(m);
    // version info
    {project.name}::py::version(m);
}}


// end of file
