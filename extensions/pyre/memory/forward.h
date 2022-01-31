// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2022 all rights reserved

// code guard
#if !defined(pyre_py_memory_forward_h)
#define pyre_py_memory_forward_h


// the {pyre} extension namespace
namespace pyre::py::memory {
    // wrapper to install a {std::shared_ptr} as the custom holder for the bindings
    template <class clsT>
    using holder_t = py::class_<clsT, std::shared_ptr<clsT>>;

    // the initializer
    void memory(py::module &);

    // bindings for file backed storage
    void maps(py::module &);

} // namespace pyre::py::memory


#endif

// end of file
