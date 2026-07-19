// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// dependencies
#include "DynamicIndexIterator.h"


// runtime-rank packing strategy: same isomorphism as Canonical<Rank> but with rank
// determined at construction time, for use in Python bindings and other dynamic contexts
//
// the packing is the map
//   Z_{s0} x ... x Z_{s_{N-1}} -> Z_{s0 * ... * s_{N-1}}
// realized by the pair {_strides}/{_nudge}, both deduced from {_shape}, {_order} and
// {_origin} under the assumption that the cells are packed tightly; the only difference
// from the compile-time flavor is that every part is a {std::vector} sized when the rank
// becomes known instead of a fixed size {std::array}
class pyre::grid::DynamicCanonical {
    // types
public:
    using size_type = size_t;
    using difference_type = std::ptrdiff_t;
    // runtime containers for each axis attribute
    using shape_type = std::vector<size_type>;
    using index_type = std::vector<difference_type>;
    using order_type = std::vector<size_type>;
    // strides are non-negative, same representation as shape
    using strides_type = std::vector<size_type>;
    // iterator
    using iterator_type = DynamicIndexIterator;

    // metamethods
public:
    // construct from shape only (zero origin, c-style order)
    explicit DynamicCanonical(const shape_type &);
    // construct from shape and origin (c-style order)
    DynamicCanonical(const shape_type &, const index_type &);
    // construct from shape, origin, and order (compute strides and nudge)
    DynamicCanonical(const shape_type &, const index_type &, const order_type &);
    // full specification: for derived layouts such as boxes and slices
    DynamicCanonical(
        const shape_type &, const index_type &, const order_type &, const strides_type &,
        difference_type);

    // default special members
public:
    ~DynamicCanonical() = default;
    DynamicCanonical(const DynamicCanonical &) = default;
    DynamicCanonical(DynamicCanonical &&) = default;
    auto operator=(const DynamicCanonical &) -> DynamicCanonical & = default;
    auto operator=(DynamicCanonical &&) -> DynamicCanonical & = default;

    // accessors
public:
    // the number of axes; a runtime property here, unlike in {Canonical} where it is a
    // compile-time constant
    [[nodiscard]] auto rank() const noexcept -> size_type;
    // the extent along each axis
    [[nodiscard]] auto shape() const noexcept -> const shape_type &;
    // the smallest addressable index
    [[nodiscard]] auto origin() const noexcept -> const index_type &;
    // the permutation that says which axis varies fastest in memory
    [[nodiscard]] auto order() const noexcept -> const order_type &;
    // the distance in memory between consecutive cells along each axis
    [[nodiscard]] auto strides() const noexcept -> const strides_type &;
    // the offset correction that places {_origin} at offset zero
    [[nodiscard]] auto nudge() const noexcept -> difference_type;
    // the number of addressable cells
    [[nodiscard]] auto cells() const noexcept -> size_type;

    // mutators: return a new instance with a different traversal order
public:
    // repack the same index box with a different packing order
    [[nodiscard]] auto order(const order_type &) const -> DynamicCanonical;

    // packing isomorphism
public:
    // map an index to the offset of its cell
    [[nodiscard]] auto offset(const index_type &) const -> difference_type;
    // the inverse: recover the index that lives at a given offset
    [[nodiscard]] auto index(difference_type) const -> index_type;
    // syntactic sugar for {offset}
    [[nodiscard]] auto operator[](const index_type &) const -> difference_type;
    // syntactic sugar for {index}
    [[nodiscard]] auto operator[](difference_type) const -> index_type;

    // iteration
public:
    // the first index in the box, in packing order
    [[nodiscard]] auto begin() const -> iterator_type;
    // the same traversal, but skipping cells according to the given step
    [[nodiscard]] auto begin(const index_type &) const -> iterator_type;
    // the sentinel that marks the end of the traversal
    [[nodiscard]] auto end() const -> iterator_type;

    // sub-layouts
public:
    // constrain to a sub-box, inheriting the physical layout
    [[nodiscard]] auto box(index_type, shape_type) const -> DynamicCanonical;
    // hyperplane extraction: fix all axes not in {free_axes} at {base}
    [[nodiscard]] auto slice(const index_type &, const std::vector<size_type> &) const
        -> DynamicCanonical;

    // implementation details
private:
    // the extent along each axis; its size is what establishes my rank
    shape_type _shape {};
    // the packing order: the axes listed from the fastest varying to the slowest
    order_type _order {};
    // the smallest addressable index; signed, so it may be negative
    index_type _origin {};
    // deduced: the memory distance between consecutive cells along each axis
    strides_type _strides {};
    // deduced: the correction that maps {_origin} to offset zero
    difference_type _nudge {};
    // deduced: the offset at which my own first cell sits
    // a layout that anchors itself is at zero here, but a derived one addresses the memory of
    // the parent it came from, so its cells begin further in; {index} measures from this mark
    difference_type _anchor {};

    // static helpers
private:
    // build the c-style permutation for a grid with the given number of axes
    static auto _defaultOrder(size_type) -> order_type;
    // deduce the strides implied by tight packing of {shape} in the given {order}
    static auto _initStrides(const shape_type &, const order_type &) -> strides_type;
    // compute the offset of {origin}, whose negation becomes the nudge
    static auto _initShift(const index_type &, const strides_type &) -> difference_type;
};


// get the inline implementations
#include "DynamicCanonical.icc"


// end of file
