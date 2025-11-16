// -*- c++ -*-
//
// bianca giovanardi
// (c) 1998-2025 all rights reserved


// code guard
#if !defined(pyre_grid_Symmetric_h)
#define pyre_grid_Symmetric_h


// encapsulation of the symmetric packing strategy
// a packing strategy provides the isomorphism
//
//    Z_s1 x ... x Z_sn -> Z_(s1 * ... * sn)
//
template <int N, typename T, template <typename, std::size_t> class containerT>
class pyre::grid::Symmetric {
    // types
public:
    // alias for me
    using symmetric_type = Symmetric<N, T, containerT>;
    using symmetric_const_reference = const symmetric_type &;
    // my parts
    // rank order
    using order_type = Order<containerT<T, N>>;
    using order_const_reference = const order_type &;
    // rank specifications
    using shape_type = Shape<containerT<T, N>>;
    using shape_const_reference = const shape_type &;
    // indices
    using index_type = Index<containerT<T, N>>;
    using index_const_reference = const index_type &;
    // offsets
    using difference_type = typename index_type::difference_type;
    // iterators
    using index_iterator = IndexIterator<symmetric_type>;

    // metamethods
public:
    // constructor (shape and origin must be diagonal indices)
    constexpr explicit Symmetric(
        shape_const_reference shape, index_const_reference origin = index_type::zero(),
        order_const_reference order = order_type::c());

    // interface
public:
    // accessors
    // user supplied
    constexpr auto shape() const -> shape_type;
    constexpr auto order() const -> order_type;
    constexpr auto origin() const -> index_type;

    // the total number of addressable cells
    constexpr auto cells() const -> T;

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

    // implementation details: static helpers for recursive index calculation
private:
    // the total number of entries in a symmetric packing of rank {M} and dimension {D}
    template <int M>
    static constexpr T _entries(T D)
        requires(M == 1);
    template <int M>
    static constexpr T _entries(T D)
        requires(M > 1);

    // the total number of entries in all ranks lower than {i} in a symmetric packing of rank {M}
    // and dimension {D}
    template <int M>
    static constexpr T _entriesBeforeRank(int i, T D);

    // the offset associated with the M-rank index {i, j...} in a symmetric packing of rank {M} and
    // dimension {D}
    template <int M, class... S>
    static constexpr auto _offset(T D, int i, S... j) -> difference_type
        requires(sizeof...(S) == M - 1 && M > 1);
    template <int M>
    static constexpr auto _offset(T D, int i) -> difference_type
        requires(M == 1);

    // the index of the first rank corresponding to {offset} in a symmetric packing of rank {M} and
    // dimension {D}
    template <int M>
    static constexpr int _getFirstRankIndex(T D, difference_type & offset)
        requires(M > 1);
    template <int M>
    static constexpr int _getFirstRankIndex(T D, difference_type & offset)
        requires(M == 1);

    // implementation details: data
private:
    // supplied by the caller
    const shape_type _shape;  // my shape
    const order_type _order;  // the packing order of the axes
    const index_type _origin; // the smallest allowable index value
    // deduced
    const T _D; // the shape dimension

    // metamethods with default implementations
public:
    // destructor
    ~Symmetric() = default;
    // constructors
    Symmetric(const Symmetric &) = default;
    Symmetric & operator=(const Symmetric &) = default;
    Symmetric(Symmetric &&) = default;
    Symmetric & operator=(Symmetric &&) = default;
};


// get the inline definitions
#define pyre_grid_Symmetric_icc
#include "Symmetric.icc"
#undef pyre_grid_Symmetric_icc


#endif

// end of file
