// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_grid_Product_h)
#define pyre_grid_Product_h


// thin wrapper over {rep_t} that serves as the base for all classes that encapsulate cartesian
// products, hence the name
//
// the client supplies:
//  - its rank {N}
//  - the category of each factor in {T}: {int}, {long}
//  - the container choice to hand down to {rep_t} that stores per-rank values
//
// note: no {crtp} here, for now...
template <class containerT>
class pyre::grid::Product : public Rep<containerT> {
    // types
public:
    // alias for me
    using product_type = Product<containerT>;
    // alias for my base
    using rep_type = Rep<containerT>;
    // the rank type determines the sets whose product we are computing
    using rank_type = typename rep_type::value_type;

    // my iterators depend on an external ordering
    template <class orderT>
    using iterator = OrderIterator<product_type, typename orderT::const_iterator, false>;

    template <class orderT>
    using const_iterator = OrderIterator<product_type, typename orderT::const_iterator, true>;

    template <class orderT>
    using reverse_iterator = OrderIterator<product_type,
                                           typename orderT::const_reverse_iterator, false>;

    template <class orderT>
    using const_reverse_iterator = OrderIterator<product_type,
                                                 typename orderT::const_reverse_iterator, true>;

    // metamethods
public:
    // constructor
    template <typename... argT>
    constexpr explicit Product(argT...);

    // iteration support
public:
    // pull the basic iterator support from my base class
    using rep_type::begin;
    using rep_type::end;
    using rep_type::rbegin;
    using rep_type::rend;
    using rep_type::cbegin;
    using rep_type::cend;
    using rep_type::crbegin;
    using rep_type::crend;

    // iterate in a given order
    template <class orderT>
    constexpr auto begin(const orderT &) -> iterator<orderT>;

    template <class orderT>
    constexpr auto begin(const orderT &) const -> const_iterator<orderT>;

    template <class orderT>
    constexpr auto end(const orderT &) -> iterator<orderT>;

    template <class orderT>
    constexpr auto end(const orderT &) const -> const_iterator<orderT>;

    // iterate in the reverse of a given order
    template <class orderT>
    constexpr auto rbegin(const orderT &) -> reverse_iterator<orderT>;

    template <class orderT>
    constexpr auto rbegin(const orderT &) const -> const_reverse_iterator<orderT>;

    template <class orderT>
    constexpr auto rend(const orderT &) -> reverse_iterator<orderT>;

    template <class orderT>
    constexpr auto rend(const orderT &) const -> const_reverse_iterator<orderT>;

    // const iteration
    template <class orderT>
    constexpr auto cbegin(const orderT &) const -> const_iterator<orderT>;

    template <class orderT>
    constexpr auto cend(const orderT &) const -> const_iterator<orderT>;

    template <class orderT>
    constexpr auto crbegin(const orderT &) const -> const_reverse_iterator<orderT>;

    template <class orderT>
    constexpr auto crend(const orderT &) const -> const_reverse_iterator<orderT>;

    // default metamethods
public:
    // destructor
    ~Product() = default;
    // constructors
    Product(const Product &) = default;
    Product(Product &&) = default;
    Product & operator=(const Product &) = default;
    Product & operator=(Product &&) = default;
};


// get the inline definitions
#define pyre_grid_Product_icc
#include "Product.icc"
#undef pyre_grid_Product_icc


#endif

// end of file
