// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"
// my base class
#include "Identifier.h"


// the description of the layout of a dataset's elements
class pyre::h5::DataSpace : public pyre::h5::Identifier {
    // types
public:
    // the kind of a dataspace: scalar, simple, or null
    using class_type = H5S_class_t;
    // the way a selection combines with the existing one
    using selection_type = H5S_seloper_t;

    // metamethods
public:
    // make a dataspace of the given {type}, scalar by default
    explicit DataSpace(class_type type = H5S_SCALAR);
    // make a simple dataspace with the given {shape}
    explicit DataSpace(const shape_t & shape);
    // adopt an existing raw handle
    explicit DataSpace(id_type id);
    // the full set of special members
    DataSpace(const DataSpace &) = default;
    DataSpace(DataSpace &&) noexcept = default;
    DataSpace & operator=(const DataSpace &) = default;
    DataSpace & operator=(DataSpace &&) noexcept = default;
    ~DataSpace() override = default;

    // static interface
public:
    // the shared dataspace that denotes the whole extent of a dataset
    static auto all() -> const DataSpace &;

    // interface: extent
public:
    // whether i have a simple, i.e. regular, extent
    auto simple() const -> bool;
    // the number of dimensions of my extent
    auto rank() const -> int;
    // my extent, one entry per dimension
    auto shape() const -> shape_t;
    // give me a new simple extent
    auto reshape(const shape_t & shape) -> void;
    // the number of cells in my extent
    auto cells() const -> hssize_t;
    // my kind
    auto type() const -> class_type;
    // discard my extent, leaving me empty
    auto clear() -> void;
    // a copy of me with the same extent and selection
    auto clone() const -> DataSpace;
    // release my handle
    auto close() -> void;

    // interface: selection
public:
    // whether my current selection lies within my extent
    auto validSelection() const -> bool;
    // the (begin, end) bounding box of my current selection
    auto selectionBounds() const -> slab_t;
    // the number of cells in my current selection
    auto selectedCells() const -> hssize_t;
    // the number of elements in my current point selection
    auto selectedElements() const -> hssize_t;
    // the number of hyperslabs in my current selection
    auto selectedSlabs() const -> hssize_t;
    // select my entire extent
    auto selectAll() -> void;
    // clear my selection
    auto selectNone() -> void;
    // shift my current selection by {delta}
    auto offset(const offsets_t & delta) -> void;
    // combine the given {elements} with my current selection using {op}
    auto selectElements(selection_type op, const points_t & elements) -> void;
    // the list of selected elements, starting at the {start}-th
    auto selectedElementList(int start = 0) const -> points_t;
    // select one slab of the given {shape} at the given {origin}
    auto slab(const index_t & origin, const shape_t & shape) -> void;
    // combine one slab of the given {shape} at {origin} with my selection using {op}
    auto slab(selection_type op, const index_t & origin, const shape_t & shape) -> void;
    // combine a fully specified strided slab with my selection using {op}
    auto slab(
        selection_type op, const shape_t & origin, const shape_t & shape, const shape_t & stride,
        const shape_t & count) -> void;
    // the list of selected hyperslabs, starting at the {start}-th
    auto selectedSlabList(int start = 0) const -> slabs_t;
};


// end of file
