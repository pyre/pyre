// -*- c++ -*-
//
// bianca giovanardi
// (c) 1998-2023 all rights reserved


// code guard
#if !defined(pyre_grid_Diagonal_h)
#define pyre_grid_Diagonal_h


// encapsulation of the diagonal packing strategy
// a packing strategy provides the isomorphism
//
//    Z_s1 x ... x Z_sn -> Z_(s1 * ... * sn)
//
template <int N, template <typename, std::size_t> class containerT>
class pyre::grid::Diagonal {
    // types
public:
    // alias for me
    using diagonal_type = Diagonal<N, containerT>;
    using diagonal_const_reference = const diagonal_type &;
    // my parts
    // rank order
    using order_type = Order<containerT<int, N>>;
    using order_const_reference = const order_type &;
    // rank specifications
    using shape_type = Shape<containerT<int, N>>;
    using shape_const_reference = const shape_type &;
    // indices
    using index_type = Index<containerT<int, N>>;
    using index_const_reference = const index_type &;
    // offsets
    using difference_type = typename index_type::difference_type;
    // iterators
    using index_iterator = IndexIterator<diagonal_type>;

    // metamethods
public:
    // constructor that deduces {_nudge}
    constexpr explicit Diagonal(
        shape_const_reference shape, index_const_reference origin = index_type::zero(),
        order_const_reference order = order_type::c());

    // interface
public:
    // accessors
    // user supplied
    constexpr auto shape() const -> shape_type;
    constexpr auto order() const -> order_type;
    constexpr auto origin() const -> index_type;
    // deduced
    constexpr auto nudge() const -> difference_type;

    // the total number of addressable cells
    constexpr auto cells() const -> std::size_t;

    // the packing isomorphism
public:
    // from a given offset to the matching index
    constexpr auto index(difference_type) const -> index_type;
    // from an index to its offset from the beginning of the array
    constexpr auto offset(index_const_reference) const -> difference_type;

    // syntactic sugar for the above
    constexpr auto operator[](difference_type) const -> index_type;
    constexpr auto operator[](index_const_reference) const -> difference_type;

    // iteration support: iterators generate sequences of indices
public:
    // whole layout iterators
    constexpr auto begin() const -> index_iterator;
    constexpr auto begin(index_const_reference step) const -> index_iterator;
    constexpr auto end() const -> index_iterator;

    // static interface
public:
    // the number of axes
    static constexpr auto rank() -> int;

    // implementation details: static helpers
protected:
    // compute the shift that maps the lowest possible index to zero offset
    static constexpr auto _initShift(index_const_reference) -> difference_type;
    // check if {index} is an index on the diagonal
    static constexpr auto _isDiagonalIndex(index_const_reference index) -> bool;

    // implementation details: data
private:
    // supplied by the caller
    const shape_type _shape;  // my shape
    const order_type _order;  // the packing order of the axes
    const index_type _origin; // the smallest allowable index value
    // deduced
    const int _D;                 // the shape dimension
    const difference_type _nudge; // offset correction when {_origin} is not {zero}

    // metamethods with default implementations
public:
    // destructor
    ~Diagonal() = default;
    // constructors
    Diagonal(const Diagonal &) = default;
    Diagonal & operator=(const Diagonal &) = default;
    Diagonal(Diagonal &&) = default;
    Diagonal & operator=(Diagonal &&) = default;
};


// get the inline definitions
#define pyre_grid_Diagonal_icc
#include "Diagonal.icc"
#undef pyre_grid_Diagonal_icc


#endif

// end of file
