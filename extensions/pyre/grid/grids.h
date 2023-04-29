// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_py_grid_grids_h)
#define pyre_py_grid_grids_h


// the {pyre} extension namespace
namespace pyre::py::grid {
    // the class record factories
    template <typename storageT, int dim>
    auto bind(py::module & m);

    template <typename storageT, int dim>
    auto bindconst(py::module & m);

    // the make of the record
    template <typename storageT, int dim>
    auto makecls(py::module & m);

    // add constructors
    template <class gridT>
    void constructors(py::class_<gridT> &);

    // write interface
    template <class gridT>
    void read(py::class_<gridT> &);

    // read interface
    template <class gridT>
    void write(py::class_<gridT> &);

    // the typename table
    static std::unordered_map<std::type_index, std::string> typenames;
} // namespace pyre::py::grid


// get the inline definitions
#define pyre_py_grid_grids_icc
#include "grids.icc"
#undef pyre_py_grid_grids_icc

#endif

// end of file
