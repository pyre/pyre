// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved

// code guard
#pragma once

// externals
#include "externals.h"
// forward declarations
#include "forward.h"


// the base class for heaps, maps, and views
// not useful on its own; it's here to support th python bindings by providing a common base class
// that can be used for type identification
template <class T, bool isConst>
class pyre::memory::Buffer {
    // types
public:
    // my cell
    using cell_type = Cell<T, isConst>;
    // pull the type aliases
    using value_type = typename cell_type::value_type;
    // derived types
    using pointer = typename cell_type::pointer;
    using const_pointer = typename cell_type::const_pointer;
    using reference = typename cell_type::reference;
    using const_reference = typename cell_type::const_reference;
    // distances
    using difference_type = typename cell_type::difference_type;
    // sizes of things
    using size_type = typename cell_type::size_type;
    using cell_count_type = typename cell_type::cell_count_type;
    // my handle
    using handle_type = std::shared_ptr<value_type[]>;
    // strings
    using uri_type = string_t;
    using string_type = string_t;

    // accessors
public:
    // expose my constness
    static constexpr auto readonly() -> bool;
    static constexpr auto writable() -> bool;

    // simulate my c++ declaration
    static inline auto declSelf() -> string_type;
    // simulate the c++ declaration of my template parameter
    static inline auto declValue() -> string_type;
    // human readable rendering of my expansion
    static inline auto className() -> string_type;

    // default metamethods
public:
    // destructor
    ~Buffer() = default;
    // constructors
    Buffer() = default;
    Buffer(const Buffer &) = default;
    Buffer(Buffer &&) = default;
    Buffer & operator=(const Buffer &) = default;
    Buffer & operator=(Buffer &&) = default;
};


// inline definitions
#include "Buffer.icc"


// end of file
