// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_memory_Stack_h)
#define pyre_memory_Stack_h


// a file-backed block of cells
template <int D, class T, bool isConst>
class pyre::memory::Stack {
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

    // my storage
    using array_type = std::array<value_type, D>;
    using iterator = std::conditional_t<
        isConst, typename array_type::const_iterator, typename array_type::iterator>;
    using const_iterator = typename array_type::const_iterator;

    // metamethods
public:
    // constructor
    inline Stack();

    // accessors
public:
    // the number of cells
    constexpr auto cells() const -> cell_count_type;
    // the memory footprint of the block
    constexpr auto bytes() const -> size_type;
    // access to the raw data pointer
    constexpr auto data() const -> pointer;

    // iterator support
public:
    constexpr auto begin() -> iterator;
    constexpr auto end() -> iterator;
    constexpr auto cbegin() const -> const_iterator;
    constexpr auto cend() const -> const_iterator;

    // data access
public:
    // with bounds checking
    inline auto at(size_type) -> reference;
    inline auto at(size_type) const -> const_reference;
    // without bounds checking
    inline auto operator[](size_type) -> reference;
    inline auto operator[](size_type) const -> const_reference;

    // implementation details: data
private:
    array_type _data;

    // default metamethods
public:
    // destructor
    ~Stack() = default;
    // constructors
    Stack(const Stack &) = default;
    Stack(Stack &&) = default;
    Stack & operator= (const Stack &) = default;
    Stack & operator= (Stack &&) = default;
};


// get the inline definitions
#define pyre_memory_Stack_icc
#include "Stack.icc"
#undef pyre_memory_Stack_icc


# endif

// end of file
