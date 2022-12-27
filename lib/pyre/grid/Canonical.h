// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_grid_Canonical_h)
#define pyre_grid_Canonical_h


// encapsulation of the canonical packing strategy
// a packing strategy provides the isomorphism
//
//    Z_s1 x ... x Z_sn -> Z_(s1 * ... * sn)
//
template <int N, template <typename, std::size_t> class containerT>
class pyre::grid::Canonical {
    // types
public:
    // alias for me
    using canonical_type = Canonical<N, containerT>;
    using canonical_const_reference = const canonical_type &;
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
    // strides are like shapes with a wide type so overflow is less likely
    using strides_type = Shape<containerT<int, N>>;
    using strides_const_reference = const strides_type &;
    // offsets
    using difference_type = typename index_type::difference_type;
    // iterators
    using index_iterator = IndexIterator<canonical_type>;

    // metamethods
public:
    // constructor that deduces {_strides} and {_nudge}
    constexpr explicit
    Canonical(shape_const_reference shape,
              index_const_reference origin = index_type::zero(),
              order_const_reference order = order_type::c());
    // constructor that requires a detailed description of the packing; useful for making slices
    constexpr
    Canonical(shape_const_reference shape,
              index_const_reference origin,
              order_const_reference order,
              strides_const_reference strides,
              difference_type nudge);

    // interface
public:
    // accessors
    // user supplied
    constexpr auto shape() const -> shape_type;
    constexpr auto order() const -> order_type;
    constexpr auto origin() const -> index_type;
    // deduced
    constexpr auto strides() const -> strides_type;
    constexpr auto nudge() const -> difference_type;

    // the total number of addressable cells
    constexpr auto cells() const -> std::size_t;

    // mutators: {canonical_type} instances are {const}, so mutators create new instances
public:
    constexpr auto order(order_const_reference) const -> canonical_type;

    // the packing isomorphism
public:
    // from a given offset to the matching index
    constexpr auto index(difference_type) const -> index_type;
    // from an index to its offset from the beginning of the array
    constexpr auto offset(index_const_reference) const -> difference_type;

    // syntactic sugar for the above
    constexpr auto operator[](difference_type) const -> index_type;
    constexpr auto operator[](index_const_reference) const -> difference_type;

    // slicing
public:
    // when the shape is known at compile time
    template <int... shape>
    constexpr auto cslice(index_const_reference base) const;
    // when only the rank of the slice is known at compile time
    template <int sliceRank = N>
    constexpr auto slice(index_const_reference base, shape_const_reference shape) const;

    // iteration support: iterators generate sequences of indices
public:
    // whole layout iterators
    constexpr auto begin() const -> index_iterator;
    constexpr auto begin(index_const_reference step) const -> index_iterator;
    constexpr auto end() const -> index_iterator;

    // use an existing layout to derive a new one
    constexpr auto
    box(index_const_reference, shape_const_reference) const -> canonical_type;

    // static interface
public:
    // the number of axes
    static constexpr auto rank() -> int;

    // implementation details: static helpers
protected:
    // given a {shape} and an {order}, infer the axis strides assuming tight packing
    static constexpr auto _initStrides(shape_const_reference,
                                       order_const_reference) -> strides_type;
    // given the packing {strides}, compute the shift that maps the lowest possible index to
    // zero offset
    static constexpr auto _initShift(index_const_reference, strides_const_reference)
        -> difference_type;

    // implementation details: data
private:
    // supplied by the caller
    const shape_type _shape;         // my shape
    const order_type _order;         // the packing order of the axes
    const index_type _origin;        // the smallest allowable index value
    // deduced
    const strides_type _strides;     // the vector of strides for axis
    const difference_type _nudge;    // offset correction when {_origin} is not {zero}

    // metamethods with default implementations
public:
    // destructor
    ~Canonical() = default;
    // constructors
    Canonical(const Canonical &) = default;
    Canonical & operator= (const Canonical &) = default;
    Canonical(Canonical &&) = default;
    Canonical & operator= (Canonical &&) = default;
};


// get the inline definitions
#define pyre_grid_Canonical_icc
#include "Canonical.icc"
#undef pyre_grid_Canonical_icc


#endif

// end of file
