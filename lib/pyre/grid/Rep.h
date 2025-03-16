// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved

// code guard
#pragma once


// thin adaptor over a compile time container that we use to store index ranks, grid shapes,
// packing order and the like; it provides an abstraction layer that is necessary for
// supporting the implementation in environments that don't have {std::array}
template <class containerT>
class pyre::grid::Rep : public containerT {
    // types
public:
    // alias for me
    using rep_type = Rep<containerT>;
    // and my container
    using container_type = containerT;
    // my value
    using value_type = typename container_type::value_type;
    using pointer = typename container_type::pointer;
    using const_pointer = typename container_type::const_pointer;
    using reference = typename container_type::reference;
    using const_reference = typename container_type::const_reference;
    // offsets
    using difference_type = typename container_type::difference_type;
    // container access
    using iterator = typename container_type::iterator;
    using const_iterator = typename container_type::const_iterator;
    using reverse_iterator = typename container_type::reverse_iterator;
    using const_reverse_iterator = typename container_type::const_reverse_iterator;

    // metamethods
public:
    // default constructor
    constexpr Rep();

    // aggregate initialization
#if defined(PYRE_GRID_SFINAE)
    template <
        // with some number of arguments
        typename... argT,
        // SFINAE: enable this constructor only
        typename = std::enable_if_t<
            // when the number of arguments in the parameter pack
            sizeof...(argT)
            // is less than or equal to
            ==
            // the size of my target {container_type}
            std::tuple_size_v<std::decay_t<container_type>>>>
    constexpr explicit Rep(argT...);
#else
    template <typename... argT>
    constexpr explicit Rep(argT...);
#endif

#if NYI_MOVE_TO_THE_BINDINGS
    // initialization
    template <typename tupleT>
    constexpr Rep(tupleT && tuple);
#endif

    // interface
public:
    // maximum and minimum
    constexpr auto max() -> value_type;
    constexpr auto min() -> value_type;

    // static interface
public:
    // my rank is the number of indices i can store
    static constexpr auto rank() -> int;
    // make a rep filled with zeroes
    static constexpr auto zero() -> rep_type;
    // a rep filled with ones
    static constexpr auto one() -> rep_type;
    // and a rep filled with some specific value
    static constexpr auto fill(const_reference) -> rep_type;

    // default metamethods
public:
    // destructor
    ~Rep() = default;
    // constructors
    Rep(const Rep &) = default;
    Rep(Rep &&) = default;
    Rep & operator=(const Rep &) = default;
    Rep & operator=(Rep &&) = default;
};


// get the inline definitions
#include "Rep.icc"


// end of file
