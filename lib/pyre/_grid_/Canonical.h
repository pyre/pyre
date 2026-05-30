// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// Canonical.h includes its dependencies directly so the type aliases in the class body
// refer to complete types; public.h includes the others in order before this file
#include "Shape.h"
#include "Index.h"
#include "Order.h"
#include "IndexIterator.h"


// the canonical packing strategy: the isomorphism
//   Z_{s0} x ... x Z_{s_{N-1}} -> Z_{s0 * ... * s_{N-1}}
// parameterized by the traversal order of the axes
template <std::size_t Rank>
class pyre::grid::Canonical {
    // types
public:
    // myself
    using self_type = Canonical<Rank>;
    // parts
    using index_type = Index<Rank>;
    using shape_type = Shape<Rank>;
    using order_type = Order<Rank>;
    // strides are non-negative axis increments; same representation as shape
    using strides_type = Shape<Rank>;
    // scalars
    using size_type = size_t;
    using difference_type = std::ptrdiff_t;
    // iterator
    using iterator_type = IndexIterator<Rank>;

    // metamethods
public:
    // primary constructor: deduce strides and nudge from shape, origin, and order
    constexpr explicit Canonical(
        const shape_type &,
        const index_type & = index_type::zero(),
        const order_type & = order_type::c()) noexcept;
    // full constructor: explicit layout specification, for derived layouts such as slices
    constexpr Canonical(
        const shape_type &,
        const index_type &,
        const order_type &,
        const strides_type &,
        difference_type) noexcept;

    // default metamethods
public:
    ~Canonical() = default;
    Canonical(const Canonical &) = default;
    Canonical(Canonical &&) = default;
    auto operator=(const Canonical &) noexcept -> self_type & = default;
    auto operator=(Canonical &&) noexcept -> self_type & = default;

    // accessors
public:
    [[nodiscard]] constexpr auto shape() const noexcept -> shape_type;
    [[nodiscard]] constexpr auto origin() const noexcept -> index_type;
    [[nodiscard]] constexpr auto order() const noexcept -> order_type;
    [[nodiscard]] constexpr auto strides() const noexcept -> strides_type;
    [[nodiscard]] constexpr auto nudge() const noexcept -> difference_type;
    [[nodiscard]] constexpr auto cells() const noexcept -> size_type;
    static consteval auto rank() noexcept -> size_type;

    // mutators: return a new {Canonical} with a different traversal order
public:
    [[nodiscard]] constexpr auto order(const order_type &) const noexcept -> self_type;

    // packing isomorphism
public:
    [[nodiscard]] constexpr auto offset(const index_type &) const noexcept -> difference_type;
    [[nodiscard]] constexpr auto index(difference_type) const noexcept -> index_type;
    // syntactic sugar
    [[nodiscard]] constexpr auto operator[](const index_type &) const noexcept -> difference_type;
    [[nodiscard]] constexpr auto operator[](difference_type) const noexcept -> index_type;

    // iteration: visit every index in the box in packing order
public:
    [[nodiscard]] constexpr auto begin() const noexcept -> iterator_type;
    [[nodiscard]] constexpr auto end() const noexcept -> iterator_type;

    // sub-layout: constrain to a sub-box, inheriting the physical layout
public:
    [[nodiscard]] constexpr auto box(index_type, shape_type) const noexcept -> self_type;

    // implementation details
private:
    shape_type _shape {};
    order_type _order {};
    index_type _origin {};
    strides_type _strides {};
    difference_type _nudge {};

    // static helpers
private:
    static constexpr auto _initStrides(const shape_type &, const order_type &) noexcept
        -> strides_type;
    static constexpr auto _initShift(const index_type &, const strides_type &) noexcept
        -> difference_type;
};


// get the inline implementations
#include "Canonical.icc"


// end of file
