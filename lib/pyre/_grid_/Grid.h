// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved

// code guard
#pragma once


// support
#include "forward.h"


// the grid
template <pyre::grid::concepts::PackingStrategy P, pyre::grid::concepts::StorageStrategy S>
class pyre::grid::Grid {
    // types
public:
    // my parts
    using packing_type = P;
    using storage_type = S;

    // cell type
    using value_type = typename S::value_type;
    using pointer = typename S::pointer;
    using const_pointer = typename S::const_pointer;
    using reference = typename S::reference;
    using const_reference = typename S::const_reference;

    // metamethods
public:
    // constructors
    // from fully formed strategies
    constexpr Grid(packing_type packing, storage_type storage);

    // in-place construction of the strategies
    template <class... PArgs, class... SArgs>
        requires(
            pyre::grid::concepts::PackingConstructible<P, PArgs...>
            && pyre::grid::concepts::StorageConstructible<S, SArgs...>)
    constexpr Grid(
        std::piecewise_construct_t, std::tuple<PArgs...> pArgs, std::tuple<SArgs...> sArgs);

    // default metamethods
public:
    // destructor
    ~Grid() = default;
    // copy/move
    Grid(const Grid &) = default;
    Grid(Grid &&) noexcept = default;
    auto operator=(const Grid &) -> Grid & = default;
    auto operator=(Grid &&) noexcept -> Grid & = default;

    // disabled metamethods
private:
    // constructors
    Grid() = delete;

    // accessors
public:
    // packing
    [[nodiscard]] constexpr auto packing() const noexcept -> const packing_type &;
    // storage strategy
    [[nodiscard]] constexpr auto storage() const noexcept -> const storage_type &;

    // implementation details - data
private:
    packing_type _packing;
    storage_type _storage;
};


// the inline implementations
#include "Grid.icc"


// end of file
