// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// support
#include <concepts>


// add to the pyre::grid namespace
namespace pyre::grid::concepts {
    // the non-negative integers: the values that measure extents and label axes
    template <class T>
    concept InZ0 = std::unsigned_integral<T>;

    // a storage strategy is anything that knows how to name and reach its cells
    // it says nothing about where those cells live, so a strategy that scatters them over
    // several blocks qualifies just as well as one that owns a single expanse
    template <class S>
    concept StorageStrategy = requires {
        // it must publish the type of the cell it holds
        typename S::value_type;
        // along with the ways to point at a cell, mutably and not
        typename S::pointer;
        typename S::const_pointer;
        // and the ways to refer to a cell, mutably and not
        typename S::reference;
        typename S::const_reference;
    };

    // a storage strategy that keeps all of its cells in one expanse, and so can hand out the
    // address of the first one
    // this is what lets a grid travel to anything that speaks raw memory
    template <class S>
    concept ContiguousStorage = StorageStrategy<S> && requires(const S s) {
        // the address of the first cell
        { s.data() };
    };

    // a packing strategy is anything that knows how to address a grid
    // it fixes an index box and says where the cell named by each of its indices lives; it is
    // deliberately silent about how that map is computed, so that packings by stride, by tile,
    // or along a space filling curve all qualify
    template <class P>
    concept PackingStrategy = requires(const P p, const typename P::index_type & i) {
        // it must publish the types it addresses with
        typename P::index_type;
        typename P::shape_type;
        typename P::size_type;
        typename P::difference_type;

        // the extent of my index box
        { p.shape() };
        // and the smallest index in it
        { p.origin() };
        // the number of axes, however it happens to be known
        { p.rank() } -> std::integral;

        // the number of cells a storage strategy must supply to hold me
        // this is not the volume of the index box: a packing that stores fewer cells than it
        // addresses, or that pads out to a tile boundary, reports what it actually needs
        { p.cells() } -> std::integral;

        // where the cell named by an index lives
        // total by construction: every index in the box has a home, even in packings that give
        // several indices the same cell, or that send the ones they do not store to a sink
        { p.offset(i) } -> std::same_as<typename P::difference_type>;

        // walking my index box
        { p.begin() };
        { p.end() };
    };

    // a packing whose offset map is injective can be run backwards
    // packings that fold several indices onto one cell, or that pad, cannot say which index a
    // given offset came from, so they are excluded
    template <class P>
    concept InvertiblePacking =
        PackingStrategy<P> && requires(const P p, typename P::difference_type off) {
            // the index of the cell that lives at a given offset
            { p.index(off) };
        };

    // a packing that addresses storage by a fixed increment per axis
    // this is the property that lets a grid be described to anything that speaks shape and
    // strides; a packing without it must be copied into one that has it before it can travel
    template <class P>
    concept StridedPacking = PackingStrategy<P> && requires(const P p) {
        // it must publish the type that carries the increments
        typename P::strides_type;
        // the increment along each axis
        { p.strides() };
        // and the correction that places my first cell
        { p.nudge() } -> std::same_as<typename P::difference_type>;
    };

    // a packing that groups its cells into tiles, each stored as a unit
    // clients that move data in bulk work a tile at a time, so they must be able to ask which
    // tile an index falls in, and how the tiles are numbered
    template <class P>
    concept TiledPacking =
        PackingStrategy<P>
        && requires(const P p, const typename P::index_type & i, const typename P::index_type & t) {
               // the extent of one tile
               { p.tileShape() };
               // the extent of the grid of tiles
               { p.tiles() };
               // the tile that a given index falls in
               { p.tileOf(i) };
               // and the number of that tile, which is how storage refers to it
               { p.tileOrdinal(t) } -> std::integral;
           };

    // the guards that let a grid build its packing in place, from a tuple of arguments
    template <class P, class... PArgs>
    concept PackingConstructible = std::constructible_from<P, PArgs...>;

    // and the matching guard for building its storage in place
    template <class S, class... SArgs>
    concept StorageConstructible = std::constructible_from<S, SArgs...>;

} // namespace pyre::grid::concepts


// end of file
