// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// DynamicCanonical includes its dependencies directly so the class body sees complete types
#include "DynamicIndexIterator.h"


// runtime-rank packing strategy: same isomorphism as Canonical<Rank> but with rank
// determined at construction time, for use in Python bindings and other dynamic contexts
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
    [[nodiscard]] auto rank() const noexcept -> size_type;
    [[nodiscard]] auto shape() const noexcept -> const shape_type &;
    [[nodiscard]] auto origin() const noexcept -> const index_type &;
    [[nodiscard]] auto order() const noexcept -> const order_type &;
    [[nodiscard]] auto strides() const noexcept -> const strides_type &;
    [[nodiscard]] auto nudge() const noexcept -> difference_type;
    [[nodiscard]] auto cells() const noexcept -> size_type;

    // mutators: return a new instance with a different traversal order
public:
    [[nodiscard]] auto order(const order_type &) const -> DynamicCanonical;

    // packing isomorphism
public:
    [[nodiscard]] auto offset(const index_type &) const -> difference_type;
    [[nodiscard]] auto index(difference_type) const -> index_type;
    [[nodiscard]] auto operator[](const index_type &) const -> difference_type;
    [[nodiscard]] auto operator[](difference_type) const -> index_type;

    // iteration
public:
    [[nodiscard]] auto begin() const -> iterator_type;
    [[nodiscard]] auto begin(const index_type &) const -> iterator_type;
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
    shape_type _shape {};
    order_type _order {};
    index_type _origin {};
    strides_type _strides {};
    difference_type _nudge {};

    // static helpers
private:
    static auto _defaultOrder(size_type) -> order_type;
    static auto _initStrides(const shape_type &, const order_type &) -> strides_type;
    static auto _initShift(const index_type &, const strides_type &) -> difference_type;
};


// get the inline implementations
#include "DynamicCanonical.icc"


// end of file
