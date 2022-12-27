// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_h5_api_h)
#define pyre_h5_api_h


// interface
namespace pyre::h5 {

    // datasets: basic IO
    // support for reading datasets into a {pyre::grid} when the correct HDF5 data type can be
    // deduced automatically
    template <class gridT>
    auto read(
        // the dataset we are reading from
        const dataset_t &,
        // the location to start reading from
        const typename gridT::index_type & origin,
        // the shape of the block
        const typename gridT::shape_type & shape,
        // and the strides
        const typename gridT::shape_type & strides) -> gridT;

    // support for reading datasets into a {pyre::grid} when the caller supplies
    // the correct HDF5 data type
    template <class gridT>
    auto read(
        // the dataset we are reading from
        const dataset_t &,
        // the type definition that describe the memory layout
        const datatype_t &,
        // the location to start reading from
        const typename gridT::index_type & origin,
        // the shape of the block
        const typename gridT::shape_type & shape,
        // and the strides
        const typename gridT::shape_type & strides) -> gridT;


} // namespace pyre::h5


#endif

// end of file
