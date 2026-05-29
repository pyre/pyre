// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved

// code guard
#pragma once


// get the external declaration
#include "externals.h"
// grab the concepts
#include "concepts.h"

// set up the namespace
namespace pyre::grid {
    // packing order
    template <size_t Rank>
    class Order;

    // shape
    template <size_t Rank>
    class Shape;

    // the grid
    template <concepts::PackingStrategy P, concepts::StorageStrategy S>
    class Grid;
} // namespace pyre::grid


// operators on {Shape}
namespace pyre::grid {
    // stream injection
    template <size_t Rank>
    auto operator<<(ostream_reference, const Shape<Rank> &) -> ostream_reference;

    // equality
    template <size_t Rank>
    constexpr auto operator==(const Shape<Rank> &, const Shape<Rank> &) noexcept -> bool;

    // component-wise arithmetic
    template <size_t Rank>
    constexpr auto operator+(const Shape<Rank> &, const Shape<Rank> &) noexcept -> Shape<Rank>;

    template <size_t Rank>
    constexpr auto operator-(const Shape<Rank> &, const Shape<Rank> &) noexcept -> Shape<Rank>;

    // scaling by integers
    template <size_t Rank>
    constexpr auto operator*(const Shape<Rank> &, int) noexcept -> Shape<Rank>;
    template <size_t Rank>
    constexpr auto operator*(int, const Shape<Rank> &) noexcept -> Shape<Rank>;
    template <size_t Rank>
    constexpr auto operator*(const Shape<Rank> &, long) noexcept -> Shape<Rank>;
    template <size_t Rank>
    constexpr auto operator*(long, const Shape<Rank> &) noexcept -> Shape<Rank>;

    // cartesian product: concatenate two shapes into one of higher rank
    template <size_t Rank1, size_t Rank2>
    constexpr auto operator*(const Shape<Rank1> &, const Shape<Rank2> &) noexcept
        -> Shape<Rank1 + Rank2>;

    // structured binding support
    template <size_t I, size_t Rank>
    constexpr auto get(Shape<Rank> &) noexcept -> typename Shape<Rank>::reference;
    template <size_t I, size_t Rank>
    constexpr auto get(Shape<Rank> &&) noexcept -> typename Shape<Rank>::rvalue_reference;
    template <size_t I, size_t Rank>
    constexpr auto get(const Shape<Rank> &) noexcept -> typename Shape<Rank>::const_reference;
    template <size_t I, size_t Rank>
    constexpr auto get(const Shape<Rank> &&) noexcept -> typename Shape<Rank>::const_rvalue_reference;
} // namespace pyre::grid


// structured binding support for {Shape}: the number of components and their type
template <std::size_t Rank>
struct std::tuple_size<pyre::grid::Shape<Rank>>;

template <std::size_t I, std::size_t Rank>
struct std::tuple_element<I, pyre::grid::Shape<Rank>>;

template <std::size_t I, std::size_t Rank>
struct std::tuple_element<I, const pyre::grid::Shape<Rank>>;


// end of file
