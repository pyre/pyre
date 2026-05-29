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

    // index
    template <size_t Rank>
    class Index;

    // the grid
    template <concepts::PackingStrategy P, concepts::StorageStrategy S>
    class Grid;
} // namespace pyre::grid


// operators on {Order}
namespace pyre::grid {
    // stream injection
    template <size_t Rank>
    auto operator<<(ostream_reference, const Order<Rank> &) -> ostream_reference;

    // equality
    template <size_t Rank>
    constexpr auto operator==(const Order<Rank> &, const Order<Rank> &) noexcept -> bool;

    // structured binding support
    template <size_t I, size_t Rank>
    constexpr auto get(Order<Rank> &) noexcept -> typename Order<Rank>::reference;
    template <size_t I, size_t Rank>
    constexpr auto get(Order<Rank> &&) noexcept -> typename Order<Rank>::rvalue_reference;
    template <size_t I, size_t Rank>
    constexpr auto get(const Order<Rank> &) noexcept -> typename Order<Rank>::const_reference;
    template <size_t I, size_t Rank>
    constexpr auto get(const Order<Rank> &&) noexcept -> typename Order<Rank>::const_rvalue_reference;
} // namespace pyre::grid


// structured binding support for {Order}: the number of components and their type
template <std::size_t Rank>
struct std::tuple_size<pyre::grid::Order<Rank>>;

template <std::size_t I, std::size_t Rank>
struct std::tuple_element<I, pyre::grid::Order<Rank>>;

template <std::size_t I, std::size_t Rank>
struct std::tuple_element<I, const pyre::grid::Order<Rank>>;


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


// operators on {Index}
namespace pyre::grid {
    // stream injection
    template <size_t Rank>
    auto operator<<(ostream_reference, const Index<Rank> &) -> ostream_reference;

    // equality
    template <size_t Rank>
    constexpr auto operator==(const Index<Rank> &, const Index<Rank> &) noexcept -> bool;

    // component-wise arithmetic
    template <size_t Rank>
    constexpr auto operator+(const Index<Rank> &, const Index<Rank> &) noexcept -> Index<Rank>;

    template <size_t Rank>
    constexpr auto operator-(const Index<Rank> &, const Index<Rank> &) noexcept -> Index<Rank>;

    // scaling by integers
    template <size_t Rank>
    constexpr auto operator*(const Index<Rank> &, int) noexcept -> Index<Rank>;
    template <size_t Rank>
    constexpr auto operator*(int, const Index<Rank> &) noexcept -> Index<Rank>;
    template <size_t Rank>
    constexpr auto operator*(const Index<Rank> &, long) noexcept -> Index<Rank>;
    template <size_t Rank>
    constexpr auto operator*(long, const Index<Rank> &) noexcept -> Index<Rank>;

    // shift by a shape
    template <size_t Rank>
    constexpr auto operator+(const Index<Rank> &, const Shape<Rank> &) noexcept -> Index<Rank>;
    template <size_t Rank>
    constexpr auto operator-(const Index<Rank> &, const Shape<Rank> &) noexcept -> Index<Rank>;

    // cartesian product: concatenate two indices into one of higher rank
    template <size_t Rank1, size_t Rank2>
    constexpr auto operator*(const Index<Rank1> &, const Index<Rank2> &) noexcept
        -> Index<Rank1 + Rank2>;

    // structured binding support
    template <size_t I, size_t Rank>
    constexpr auto get(Index<Rank> &) noexcept -> typename Index<Rank>::reference;
    template <size_t I, size_t Rank>
    constexpr auto get(Index<Rank> &&) noexcept -> typename Index<Rank>::rvalue_reference;
    template <size_t I, size_t Rank>
    constexpr auto get(const Index<Rank> &) noexcept -> typename Index<Rank>::const_reference;
    template <size_t I, size_t Rank>
    constexpr auto get(const Index<Rank> &&) noexcept -> typename Index<Rank>::const_rvalue_reference;
} // namespace pyre::grid


// structured binding support for {Index}: the number of components and their type
template <std::size_t Rank>
struct std::tuple_size<pyre::grid::Index<Rank>>;

template <std::size_t I, std::size_t Rank>
struct std::tuple_element<I, pyre::grid::Index<Rank>>;

template <std::size_t I, std::size_t Rank>
struct std::tuple_element<I, const pyre::grid::Index<Rank>>;


// end of file
