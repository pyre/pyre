// -*- c++ -*-
//
// {project.authors}
// (c) {project.span} all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"

// the {project.name} library
#include <{project.name}/version.h>


// access to the version tags from the headers and the library
void
{project.name}::py::version(py::module & m)
{{
    // make a {{version}} submodule
    auto version = m.def_submodule(
        // its name
        "version",
        // its docstring
        "the static and dynamic version of the bindings");


    // add the static version
    version.def(
        // the name
        "static",
        // the implementation
        []() {{
            // build a tuple from the static info in the headers
            auto extver = std::make_tuple(
                {project.name}::version::major,
                {project.name}::version::minor,
                {project.name}::version::micro,
                {project.name}::version::revision);
            // all done
            return extver;
        }},
        // the docstring
        "the {project.name} version visible at compile time");


    // add the dynamic version
    version.def(
        // the name
        "dynamic",
        // the implementation
        []() {{
            // get the version as known to the {project.name} shared library
            auto version = {project.name}::version::version();
            // make a tuple
            auto libver = std::make_tuple(
                version.major,
                version.minor,
                version.micro,
                version.revision);
            // all done
            return libver;
        }},
        // the docstring
        "the {project.name} version visible through its shared library");


    // all done
    return;
}}


// end of file
