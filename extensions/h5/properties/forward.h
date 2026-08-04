// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// externals
#include "../external.h"


// the local binders
namespace pyre::h5::py::properties {
    // the generic base
    void pl(py::module &);
    // the properties shared by everything one creates
    void ocpl(py::module &);
    // the properties shared by everything that lays down a name
    void strcpl(py::module &);
    // dataset access, creation, and transfer
    void dapl(py::module &);
    void dcpl(py::module &);
    void dxpl(py::module &);
    // file access and creation
    void fapl(py::module &);
    void fcpl(py::module &);
    // group creation
    void gcpl(py::module &);
    // link access and creation
    void lapl(py::module &);
    void lcpl(py::module &);
    // attribute creation
    void acpl(py::module &);
} // namespace pyre::h5::py::properties


// end of file
