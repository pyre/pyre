// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// datatypes
namespace pyre::h5 {
    // the generic case
    template <typename cellT>
    inline auto datatype() -> datatype_t;

    // and its specializations for unsigned integral types
    template <>
    inline auto datatype<std::uint8_t>() -> datatype_t;
    template <>
    inline auto datatype<std::uint16_t>() -> datatype_t;
    template <>
    inline auto datatype<std::uint32_t>() -> datatype_t;
    template <>
    inline auto datatype<std::uint64_t>() -> datatype_t;
    // signed integral types
    template <>
    inline auto datatype<std::int8_t>() -> datatype_t;
    template <>
    inline auto datatype<std::int16_t>() -> datatype_t;
    template <>
    inline auto datatype<std::int32_t>() -> datatype_t;
    template <>
    inline auto datatype<std::int64_t>() -> datatype_t;
    // floating point types
    template <>
    inline auto datatype<float>() -> datatype_t;
    template <>
    inline auto datatype<double>() -> datatype_t;
    // complex types
    template <>
    inline auto datatype<std::complex<float>>() -> datatype_t;
    template <>
    inline auto datatype<std::complex<double>>() -> datatype_t;
    template <>
    inline auto datatype<std::complex<std::uint8_t>>() -> datatype_t;
    template <>
    inline auto datatype<std::complex<std::uint16_t>>() -> datatype_t;
    template <>
    inline auto datatype<std::complex<std::uint32_t>>() -> datatype_t;
    template <>
    inline auto datatype<std::complex<std::uint64_t>>() -> datatype_t;
    template <>
    inline auto datatype<std::complex<std::int8_t>>() -> datatype_t;
    template <>
    inline auto datatype<std::complex<std::int16_t>>() -> datatype_t;
    template <>
    inline auto datatype<std::complex<std::int32_t>>() -> datatype_t;
    template <>
    inline auto datatype<std::complex<std::int64_t>>() -> datatype_t;

} // namespace pyre::h5

// interface
namespace pyre::h5 {

    // datasets: basic IO
    // support for reading datasets into a {pyre::grid} when the correct HDF5 data type can be
    // deduced automatically
    template <class gridT>
    inline auto read(
        // the dataset we are reading from
        const dataset_t &,
        // the location to start reading from
        const typename gridT::index_type & origin,
        // the shape of the block
        const typename gridT::shape_type & shape,
        // and the strides
        const typename gridT::index_type & stride) -> gridT;

    // support for reading datasets into a {pyre::grid} when the caller supplies
    // the correct HDF5 data type
    template <class gridT>
    inline auto read(
        // the dataset we are reading from
        const dataset_t &,
        // the type definition that describe the memory layout
        const datatype_t &,
        // the location to start reading from
        const typename gridT::index_type & origin,
        // the shape of the block
        const typename gridT::shape_type & shape,
        // and the strides
        const typename gridT::index_type & stride) -> gridT;

    // support for reading into existing {pyre::memory} buffers
    template <class memT>
    inline auto read(
        const dataset_t & self, memT & data, const datatype_t & memtype, const shape_t & origin,
        const shape_t & shape) -> void;

    // support for reading into existing {pyre::grid} instances
    template <class gridT>
    inline auto readGrid(
        const dataset_t & self, gridT & data, const datatype_t & memtype, const shape_t & origin,
        const shape_t & shape) -> void;

    // support for writing from existing {pyre::memory} buffers
    template <class memT>
    inline auto write(
        const dataset_t & self, memT & data, const datatype_t & memtype, const shape_t & origin,
        const shape_t & shape) -> void;

    // support for writing from existing {pyre::grid} instances
    template <class gridT>
    inline auto writeGrid(
        const dataset_t & self, gridT & data, const datatype_t & memtype, const shape_t & origin,
        const shape_t & shape) -> void;

} // namespace pyre::h5


// end of file
