// -*- c++ -*-
//
// {project.authors}
// (c) {project.span} all rights reserved

// code guard
#if !defined({project.name}_py_forward_h)
#define {project.name}_py_forward_h


// the {{project.name}} namespace
namespace {project.name}::py {{
    // bindings of opaque types
    void opaque(py::module &);
    // exceptions
    void exceptions(py::module &);

    // version info
    void version(py::module &);
}}


#endif

// end of file
