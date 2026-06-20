// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#if !defined(h5_py_types_forward_h)
#define h5_py_types_forward_h


// the helpers
#include "../attributes.h"

// the local binders
namespace pyre::h5::py::types {
    // datatype classes
    void datatype(py::module &);
    void array(py::module &);
    void atom(py::module &);
    void float_(py::module &);
    void int_(py::module &);
    void predefined(py::module &);
    void str(py::module &);
    void compound(py::module &);
    void enum_(py::module &);
    void varlen(py::module &);

    // subpackages
    void native(py::module &); // native

    void std(py::module &);    // native
    void big(py::module &);    // big endian
    void little(py::module &); // little endian

    void alpha(py::module &); // native
    void ieee(py::module &);  // IEEE floating point
    void intel(py::module &); // intel specific types
    void mips(py::module &);  // intel specific types
    void unix(py::module &);  // unix

} // namespace pyre::h5::py::types


#endif

// end of file
