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

// base class
#include "Buffer.h"


// a block of cells on the heap
template <class T, bool isConst>
class pyre::memory::Heap : public Buffer<T, isConst> {
    // types
public:
    // me
    using self_type = Heap<T, isConst>;
    // my base class
    using super_type = Buffer<T, isConst>;

    // my cell
    using typename super_type::cell_type;
    // pull the type aliases
    using typename super_type::value_type;
    // derived types
    using typename super_type::pointer;
    using typename super_type::const_pointer;
    using typename super_type::reference;
    using typename super_type::const_reference;
    // distances
    using typename super_type::difference_type;
    // sizes of things
    using typename super_type::size_type;
    using typename super_type::cell_count_type;
    // my handle
    using typename super_type::handle_type;
    // strings
    using typename super_type::uri_type;
    using typename super_type::string_type;

    // metamethods
public:
    // allocate a new block of memory
    inline Heap(cell_count_type);
    // i can make one from a block and a count
    inline Heap(handle_type, cell_count_type);

    // accessors
public:
    // human readable form of my location
    inline auto uri() const -> uri_type;
    // the number of cells
    inline auto cells() const -> cell_count_type;
    // the memory footprint of the block
    inline auto bytes() const -> size_type;
    // access to the raw data pointer
    inline auto data() const -> pointer;
    // access to the raw data pointer in a form suitable for including in diagnostics
    inline auto where() const -> const void *;
    // the shared pointer
    inline auto handle() const -> handle_type;

    // expose my constness
    static constexpr auto readonly() -> bool;
    static constexpr auto writable() -> bool;

    // simulate my c++ declaration
    static inline auto declSelf() -> string_type;
    // simulate the c++ declaration of my template parameter
    static inline auto declValue() -> string_type;
    // human readable name for my type
    static inline auto className() -> string_type;

    // iterator support
public:
    inline auto begin() const -> pointer;
    inline auto end() const -> pointer;

    // data access
public:
    // with bounds checking
    inline auto at(size_type) const -> reference;
    // without bounds checking
    inline auto operator[](size_type) const -> reference;

    // implementation details: data
private:
    handle_type _data;
    const cell_count_type _cells;

    // default metamethods
public:
    // destructor
    ~Heap() = default;
    // constructors
    Heap(const Heap &) = default;
    Heap(Heap &&) = default;
    Heap & operator=(const Heap &) = default;
    Heap & operator=(Heap &&) = default;
};


// inline definitions
#include "Heap.icc"


// end of file
