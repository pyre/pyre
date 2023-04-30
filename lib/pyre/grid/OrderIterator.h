// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_grid_OrderIterator_h)
#define pyre_grid_OrderIterator_h


// an iterator that enables visiting product ranks in a specific order
template <class productT, class orderIteratorT, bool isConst>
class pyre::grid::OrderIterator : public iterator_base<productT, isConst> {
    // types
public:
    // aliases for my template parameters
    using product_type = productT;
    using order_const_iterator = orderIteratorT;
    // aliases for me
    using iterator = OrderIterator<product_type, order_const_iterator, isConst>;
    using iterator_reference = iterator &;
    // my base class
    using iterbase = iterator_base<product_type, isConst>;
    // my parts
    using order_const_iterator_reference = const order_const_iterator &;
    using product_reference = std::conditional_t<isConst, const product_type &, product_type &>;

    // what i point to
    using value_type = typename iterbase::value_type;
    using pointer = typename iterbase::pointer;
    using reference = typename iterbase::reference;

    // metamethods
public:
    constexpr OrderIterator(product_reference, order_const_iterator_reference);

    // iterator protocol
public:
    // dereference
    constexpr auto operator*() const -> reference;
    // arithmetic
    constexpr auto operator++() -> iterator_reference;
    constexpr auto operator++(int) -> iterator;

    // accessors: needed for the implementation of {operator==}
public:
    constexpr auto product() const -> product_reference;
    constexpr auto order() const -> order_const_iterator_reference;

    // implementation details: data
private:
    product_reference _product;
    order_const_iterator _order;
    // default metamethods
public:
    // destructor
    ~OrderIterator() = default;
    // let the compiler write the rest
    constexpr OrderIterator(const OrderIterator &) = default;
    constexpr OrderIterator(OrderIterator &&) = default;
    constexpr OrderIterator & operator=(const OrderIterator &) = default;
    constexpr OrderIterator & operator=(OrderIterator &&) = default;
};


// get the inline definitions
#define pyre_grid_OrderIterator_icc
#include "OrderIterator.icc"
#undef pyre_grid_OrderIterator_icc


#endif

// end of file
