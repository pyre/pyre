// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// the package global declarations
#include "../__init__.h"
// the local declarations
#include "__init__.h"
// namespace setup
#include "forward.h"


// make the namespace of the datatypes, and register their classes in it, so that every signature
// can name them
void
pyre::h5::py::types::classes(py::module & m)
{
    // make a new namespace to hold datatype descriptions
    auto types = m.def_submodule(
        // the name of the module
        "types",
        // its docstring
        "HDF5 datatypes");

    // the base datatype, before the ones that derive from it
    datatypeClass(types);
    // array datatypes
    arrayClass(types);
    // the atomic datatypes, before the ones that derive from them
    atomClass(types);
    floatClass(types);
    intClass(types);
    predefinedClass(types);
    strClass(types);
    // compound datatypes
    compoundClass(types);
    // enum types
    enumClass(types);
    // and variable length types
    varlenClass(types);

    // all done
    return;
}


// the datatypes
void
pyre::h5::py::types::__init__(py::module & m)
{
    // the namespace, made by {classes}
    auto types = m.attr("types").cast<py::module>();

    // the base datatype
    datatype();
    // array datatypes
    array();
    // the atomic datatypes
    atom();
    float_();
    int_();
    str();
    // compound datatypes
    compound();
    // enum types
    enum_();
    // variable length types
    varlen();

    // the predefined datatypes: the native ones
    native(types);
    // the standard ones, and those of either byte order
    std(types);
    big(types);
    little(types);
    // and the ones specific to a platform or a standard
    alpha(types);
    ieee(types);
    intel(types);
    mips(types);
    unix(types);

    // all done
    return;
}


// end of file
