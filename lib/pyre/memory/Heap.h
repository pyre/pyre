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


// a block of cells on the heap
template <class T, bool isConst>
class pyre::memory::Heap {
    // types
public:
    // my cell
    using cell_type = cell_t<T, isConst>;
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
    // human readable rendering of my expansion
    static inline auto name() -> string_t;
    // human readable rendering of my storage strategy
    static inline auto strategyName() -> string_t;
    // human readable rendering of my {cell_type}
    static inline auto cellName() -> string_t;
    // my {cell_type} decl
    static inline auto cellDecl() -> string_t;

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
