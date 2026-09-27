// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// code guard
#pragma once


// the structures of the dlpack exchange protocol that grids export, as specified by dlpack 1.3,
// https://github.com/dmlc/dlpack/blob/v1.3/include/dlpack/dlpack.h; the layout of each one is
// part of the protocol, so it matches the specification member for member
namespace pyre::py::grid {
    // the version of the protocol i produce
    inline constexpr std::uint32_t dlpackMajor = 1;
    inline constexpr std::uint32_t dlpackMinor = 3;

    // the flag that marks the cells of a versioned tensor as read only
    inline constexpr std::uint64_t dlpackReadOnly = 1UL << 0UL;

    // the version of the protocol a tensor was built by
    struct DLPackVersion {
        // the major version
        std::uint32_t major;
        // the minor version
        std::uint32_t minor;
    };

    // the kinds of devices whose memory a tensor may describe; only the ones grids live on
    enum DLDeviceType : std::int32_t {
        // ordinary host memory
        kDLCPU = 1,
        // cuda device memory
        kDLCUDA = 2,
        // cuda pinned host memory
        kDLCUDAHost = 3,
        // cuda managed memory
        kDLCUDAManaged = 13,
    };

    // the device a tensor lives on
    struct DLDevice {
        // its kind
        DLDeviceType device_type;
        // its ordinal among the devices of its kind
        std::int32_t device_id;
    };

    // the families of cell types; only the ones grids hold
    enum DLDataTypeCode : std::uint8_t {
        // signed integers
        kDLInt = 0U,
        // unsigned integers
        kDLUInt = 1U,
        // floating point numbers
        kDLFloat = 2U,
        // complex numbers
        kDLComplex = 5U,
    };

    // the type of a cell
    struct DLDataType {
        // its family, one of {DLDataTypeCode}
        std::uint8_t code;
        // its width, in bits
        std::uint8_t bits;
        // the number of lanes, for vector types
        std::uint16_t lanes;
    };

    // the description of a block of cells
    struct DLTensor {
        // the address of the block
        void * data;
        // the device it lives on
        DLDevice device;
        // the number of axes
        std::int32_t ndim;
        // the type of its cells
        DLDataType dtype;
        // the extent along each axis
        std::int64_t * shape;
        // the distance between consecutive cells along each axis, in cells
        std::int64_t * strides;
        // the distance from {data} to the first cell, in bytes
        std::uint64_t byte_offset;
    };

    // a tensor with a way to release it, as the protocol handed it out before it was versioned
    struct DLManagedTensor {
        // the description of the cells
        DLTensor dl_tensor;
        // whatever the producer needs to keep the cells alive
        void * manager_ctx;
        // the function the consumer calls when it is done with the tensor
        void (*deleter)(DLManagedTensor * self);
    };

    // a tensor with a way to release it, a version, and flags
    struct DLManagedTensorVersioned {
        // the version of the protocol that built it
        DLPackVersion version;
        // whatever the producer needs to keep the cells alive
        void * manager_ctx;
        // the function the consumer calls when it is done with the tensor
        void (*deleter)(DLManagedTensorVersioned * self);
        // the properties of the cells, such as {dlpackReadOnly}
        std::uint64_t flags;
        // the description of the cells
        DLTensor dl_tensor;
    };
} // namespace pyre::py::grid


// end of file
