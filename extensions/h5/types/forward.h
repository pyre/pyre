// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// the helpers
#include "../attributes.h"

// the local binders
namespace pyre::h5::py::types {
    // register the datatype classes
    void datatypeClass(py::module &);
    void arrayClass(py::module &);
    void atomClass(py::module &);
    void floatClass(py::module &);
    void intClass(py::module &);
    void predefinedClass(py::module &);
    void strClass(py::module &);
    void compoundClass(py::module &);
    void enumClass(py::module &);
    void varlenClass(py::module &);

    // bind the datatype classes; the predefined ones have nothing beyond what they inherit
    void datatype();
    void array();
    void atom();
    void float_();
    void int_();
    void str();
    void compound();
    void enum_();
    void varlen();

    // the namespaces of the predefined datatypes: the native ones
    void native(py::module &);
    // the standard ones, and those of either byte order
    void std(py::module &);
    void big(py::module &);
    void little(py::module &);
    // the ones specific to a platform or a standard
    void alpha(py::module &);
    void ieee(py::module &);
    void intel(py::module &);
    void mips(py::module &);
    void unix(py::module &);

} // namespace pyre::h5::py::types


// end of file
