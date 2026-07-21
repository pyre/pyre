// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// get the external declaration
#include "externals.h"
// grab the concepts
#include "concepts.h"

// set up the namespace
namespace pyre::grid {
    // a permutation of the axis labels that says which axis varies fastest in memory
    template <size_t Rank>
    class Order;

    // the extent of a grid along each one of its axes
    template <size_t Rank>
    class Shape;

    // a signed coordinate into a grid; signed because it may sit below the origin
    template <size_t Rank>
    class Index;

    // a generator of the sequence of indices that visits every point in a box
    template <size_t Rank>
    class IndexIterator;

    // the packing strategy that maps index space to memory offsets using strides
    template <size_t Rank>
    class Canonical;

    // the packing strategy that stores only the main diagonal
    template <size_t Rank>
    class Diagonal;

    // dynamic (runtime-rank) variants for Python interoperability
    class DynamicIndexIterator;
    class DynamicCanonical;

    // a packing strategy composed with a storage strategy
    template <concepts::PackingStrategy P, concepts::StorageStrategy S>
    class Grid;

    // a cursor that visits the cells of a grid, rather than the indices that name them
    template <class gridT>
    class GridIterator;
} // namespace pyre::grid


// operators on {GridIterator}
namespace pyre::grid {
    // equality: two cursors are equal when they have reached the same index
    template <class gridT>
    constexpr auto operator==(const GridIterator<gridT> &, const GridIterator<gridT> &) noexcept
        -> bool;

    // and the negation, so that the usual {begin} to {end} loop reads naturally
    template <class gridT>
    constexpr auto operator!=(const GridIterator<gridT> &, const GridIterator<gridT> &) noexcept
        -> bool;
} // namespace pyre::grid


// operators on {IndexIterator}
namespace pyre::grid {
    // equality: two iterators are equal when they point to the same index
    template <size_t Rank>
    constexpr auto operator==(const IndexIterator<Rank> &, const IndexIterator<Rank> &) noexcept
        -> bool;
} // namespace pyre::grid


// operators on {Order}
namespace pyre::grid {
    // render the permutation in human readable form
    template <size_t Rank>
    auto operator<<(ostream_reference, const Order<Rank> &) -> ostream_reference;

    // two orders match when they rank the axes the same way
    template <size_t Rank>
    constexpr auto operator==(const Order<Rank> &, const Order<Rank> &) noexcept -> bool;

    // let clients unpack an order into its axis labels
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
    // render the extents in human readable form
    template <size_t Rank>
    auto operator<<(ostream_reference, const Shape<Rank> &) -> ostream_reference;

    // two shapes match when they have the same extent along every axis
    template <size_t Rank>
    constexpr auto operator==(const Shape<Rank> &, const Shape<Rank> &) noexcept -> bool;

    // grow and shrink a shape one axis at a time
    template <size_t Rank>
    constexpr auto operator+(const Shape<Rank> &, const Shape<Rank> &) noexcept -> Shape<Rank>;

    template <size_t Rank>
    constexpr auto operator-(const Shape<Rank> &, const Shape<Rank> &) noexcept -> Shape<Rank>;

    // pass a shape through unchanged, or reflect it through the origin
    template <size_t Rank>
    constexpr auto operator+(const Shape<Rank> &) noexcept -> Shape<Rank>;
    template <size_t Rank>
    constexpr auto operator-(const Shape<Rank> &) noexcept -> Shape<Rank>;

    // magnify a shape uniformly while keeping it a whole number of cells
    template <size_t Rank>
    constexpr auto operator*(const Shape<Rank> &, int) noexcept -> Shape<Rank>;
    template <size_t Rank>
    constexpr auto operator*(int, const Shape<Rank> &) noexcept -> Shape<Rank>;
    template <size_t Rank>
    constexpr auto operator*(const Shape<Rank> &, long) noexcept -> Shape<Rank>;
    template <size_t Rank>
    constexpr auto operator*(long, const Shape<Rank> &) noexcept -> Shape<Rank>;

    // subdivide a shape uniformly, truncating towards zero
    template <size_t Rank>
    constexpr auto operator/(const Shape<Rank> &, int) noexcept -> Shape<Rank>;
    template <size_t Rank>
    constexpr auto operator/(const Shape<Rank> &, long) noexcept -> Shape<Rank>;

    // scaling by reals, which promotes the result to a real-valued tuple
    template <size_t Rank>
    constexpr auto operator*(const Shape<Rank> &, double) noexcept -> doubles_t<Rank>;
    template <size_t Rank>
    constexpr auto operator*(double, const Shape<Rank> &) noexcept -> doubles_t<Rank>;
    template <size_t Rank>
    constexpr auto operator/(const Shape<Rank> &, double) noexcept -> doubles_t<Rank>;
    template <size_t Rank>
    constexpr auto operator*(const Shape<Rank> &, float) noexcept -> floats_t<Rank>;
    template <size_t Rank>
    constexpr auto operator*(float, const Shape<Rank> &) noexcept -> floats_t<Rank>;
    template <size_t Rank>
    constexpr auto operator/(const Shape<Rank> &, float) noexcept -> floats_t<Rank>;

    // cartesian product: concatenate two shapes into one of higher rank
    template <size_t Rank1, size_t Rank2>
    constexpr auto operator*(const Shape<Rank1> &, const Shape<Rank2> &) noexcept
        -> Shape<Rank1 + Rank2>;

    // let clients unpack a shape into its per-axis extents
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
    // render the coordinates in human readable form
    template <size_t Rank>
    auto operator<<(ostream_reference, const Index<Rank> &) -> ostream_reference;

    // two indices match when they name the same point
    template <size_t Rank>
    constexpr auto operator==(const Index<Rank> &, const Index<Rank> &) noexcept -> bool;

    // displace one index by another, one axis at a time
    template <size_t Rank>
    constexpr auto operator+(const Index<Rank> &, const Index<Rank> &) noexcept -> Index<Rank>;

    template <size_t Rank>
    constexpr auto operator-(const Index<Rank> &, const Index<Rank> &) noexcept -> Index<Rank>;

    // pass an index through unchanged, or reflect it through the origin
    template <size_t Rank>
    constexpr auto operator+(const Index<Rank> &) noexcept -> Index<Rank>;
    template <size_t Rank>
    constexpr auto operator-(const Index<Rank> &) noexcept -> Index<Rank>;

    // stretch an index away from the origin while it remains a lattice point
    template <size_t Rank>
    constexpr auto operator*(const Index<Rank> &, int) noexcept -> Index<Rank>;
    template <size_t Rank>
    constexpr auto operator*(int, const Index<Rank> &) noexcept -> Index<Rank>;
    template <size_t Rank>
    constexpr auto operator*(const Index<Rank> &, long) noexcept -> Index<Rank>;
    template <size_t Rank>
    constexpr auto operator*(long, const Index<Rank> &) noexcept -> Index<Rank>;

    // pull an index towards the origin, truncating towards zero
    template <size_t Rank>
    constexpr auto operator/(const Index<Rank> &, int) noexcept -> Index<Rank>;
    template <size_t Rank>
    constexpr auto operator/(const Index<Rank> &, long) noexcept -> Index<Rank>;

    // scaling by reals, which promotes the result to a real-valued tuple
    template <size_t Rank>
    constexpr auto operator*(const Index<Rank> &, double) noexcept -> doubles_t<Rank>;
    template <size_t Rank>
    constexpr auto operator*(double, const Index<Rank> &) noexcept -> doubles_t<Rank>;
    template <size_t Rank>
    constexpr auto operator/(const Index<Rank> &, double) noexcept -> doubles_t<Rank>;
    template <size_t Rank>
    constexpr auto operator*(const Index<Rank> &, float) noexcept -> floats_t<Rank>;
    template <size_t Rank>
    constexpr auto operator*(float, const Index<Rank> &) noexcept -> floats_t<Rank>;
    template <size_t Rank>
    constexpr auto operator/(const Index<Rank> &, float) noexcept -> floats_t<Rank>;

    // step an index across a whole box, which is how the end of a traversal is named
    template <size_t Rank>
    constexpr auto operator+(const Index<Rank> &, const Shape<Rank> &) noexcept -> Index<Rank>;
    template <size_t Rank>
    constexpr auto operator-(const Index<Rank> &, const Shape<Rank> &) noexcept -> Index<Rank>;

    // cartesian product: concatenate two indices into one of higher rank
    template <size_t Rank1, size_t Rank2>
    constexpr auto operator*(const Index<Rank1> &, const Index<Rank2> &) noexcept
        -> Index<Rank1 + Rank2>;

    // let clients unpack an index into its per-axis coordinates
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
