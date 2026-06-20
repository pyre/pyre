// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#if !defined(h5_py_properties_forward_h)
#define h5_py_properties_forward_h


// externals
#include "../external.h"


// the local binders
namespace pyre::h5::py::properties {
    // the generic base
    void pl(py::module &);
    // dataset access, creation, and transfer
    void dapl(py::module &);
    void dcpl(py::module &);
    void dxpl(py::module &);
    // file access and creation
    void fapl(py::module &);
    void fcpl(py::module &);
    // link access and creation
    void lapl(py::module &);
    void lcpl(py::module &);
} // namespace pyre::h5::py::properties


#endif

// end of file
