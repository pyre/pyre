// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved

// code guard
#if !defined(pyre_memory_View_h)
#define pyre_memory_View_h


// a block of cells whose memory belongs to someone else
template <class T, bool isConst>
class pyre::memory::View {
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
    // strings
    using uri_type = string_t;
    using string_type = string_t;

    // metamethods
public:
    // map an existing data product
    inline View(pointer, cell_count_type);

    // interface
public:
    // human readable form of my location
    inline auto uri() const -> uri_type;
    // the number of cells
    inline auto cells() const -> cell_count_type;
    // the memory footprint of the block
    inline auto bytes() const -> size_type;
    // access to the raw data pointer
    inline auto data() const -> pointer;
    // access to the raw data pointer in a form suitable for diagnostics
    inline auto where() const -> const void *;

    // expose my constness
    static constexpr auto readonly() -> bool;
    static constexpr auto writable() -> bool;
    // human readable rendering of my expansion
    static inline auto name() -> string_type;
    // human readable rendering of my storage strategy
    static inline auto strategyName() -> string_type;
    // human readable rendering of my {cell_type}
    static inline auto cellName() -> string_type;

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
    const pointer _data;
    const cell_count_type _cells;

    // default metamethods
public:
    // destructor
    ~View() = default;
    // constructors
    View(const View &) = default;
    View(View &&) = default;
    View & operator=(const View &) = default;
    View & operator=(View &&) = default;
};


// get the inline definitions
#define pyre_memory_View_icc
#include "View.icc"
#undef pyre_memory_View_icc


#endif

// end of file
