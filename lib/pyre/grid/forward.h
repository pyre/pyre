// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_grid_forward_h)
#define pyre_grid_forward_h


// useful instantiations of STL entities
namespace pyre::grid {
    // polymorphic base class for building iterators
    template <class containerT, bool isConst>
    class iterator_base {
    public:
        using iterator_category = std::forward_iterator_tag;
        using value_type = typename containerT::value_type;
        using difference_type = typename containerT::difference_type;
        using pointer = std::conditional_t<
            isConst, typename containerT::const_pointer, typename containerT::pointer>;
        using reference = std::conditional_t<
            isConst, typename containerT::const_reference, typename containerT::reference>;
    };

    // the base class for {IndexIterator}
    template <class packingT>
    class base_index_iterator {
    public:
        using iterator_category = std::forward_iterator_tag;
        using value_type = typename packingT::index_type;
        using difference_type = void;
        using pointer = const typename packingT::index_type *;
        using reference = const typename packingT::index_type &;
    };
} // namespace pyre::grid

// set up the namespace
namespace pyre::grid {
    // thin adaptor over a compile time container
    template <class containerT>
    class Rep;
    // basic representation of our multi-dimensional entities
    template <class containerT>
    class Product;
    // shapes: the number of possible values of each index
    template <class containerT>
    class Shape;
    // indices
    template <class containerT>
    class Index;
    // index rank ordering, e.g. the order in which index axes are packed in memory
    template <class containerT>
    class Order;
    // support for visiting ranks in a specific order
    template <class productT, class orderIteratorT, bool isConst>
    class OrderIterator;

    // support for the canonical packing strategies
    // an ordered index generator
    template <class packingT>
    class IndexIterator;
    // the packing strategy
    template <int N, template <typename, std::size_t> class containerT>
    class Canonical;

    // bringing it all together
    template <class packingT, class storageT>
    class Grid;
    // and its iterator
    template <class gridT, class indexIteratorT, bool isConst>
    class GridIterator;
} // namespace pyre::grid


// operators on rep
namespace pyre::grid {
    // stream injection
    template <class containerT>
    inline auto operator<<(ostream_reference, const Rep<containerT> &) -> ostream_reference;

    // arithmetic
    // unary operators
    template <class containerT>
    constexpr auto operator+(const Rep<containerT> &) -> Rep<containerT>;

    template <class containerT>
    constexpr auto operator-(const Rep<containerT> &) -> Rep<containerT>;


    // addition
    template <class containerT>
    constexpr auto operator+(const Rep<containerT> &, const Rep<containerT> &) -> Rep<containerT>;

    // subtraction
    template <class containerT>
    constexpr auto operator-(const Rep<containerT> &, const Rep<containerT> &) -> Rep<containerT>;

    // cartesian products
    template <
        class containerT1, class containerT2,
        template <typename, std::size_t> class containerY = std::array>
    constexpr auto operator*(const Rep<containerT1> &, const Rep<containerT2> &)
        -> Rep<containerY<int, std::tuple_size_v<containerT1> + std::tuple_size_v<containerT2>>>;

    // scaling by integers
    template <class containerT>
    constexpr auto operator*(int, const Rep<containerT> &) -> Rep<containerT>;

    template <class containerT>
    constexpr auto operator*(const Rep<containerT> &, int) -> Rep<containerT>;

    template <class containerT>
    constexpr auto operator/(const Rep<containerT> &, int) -> Rep<containerT>;

    // scaling by doubles
    template <class containerT>
    constexpr auto operator*(double, const Rep<containerT> &) -> doubles_t<Rep<containerT>::rank()>;

    template <class containerT>
    constexpr auto operator*(const Rep<containerT> &, double) -> doubles_t<Rep<containerT>::rank()>;

    template <class containerT>
    constexpr auto operator/(const Rep<containerT> &, double) -> doubles_t<Rep<containerT>::rank()>;

    // scaling by floats
    template <class containerT>
    constexpr auto operator*(float, const Rep<containerT> &) -> floats_t<Rep<containerT>::rank()>;

    template <class containerT>
    constexpr auto operator*(const Rep<containerT> &, float) -> floats_t<Rep<containerT>::rank()>;

    template <class containerT>
    constexpr auto operator/(const Rep<containerT> &, float) -> floats_t<Rep<containerT>::rank()>;
} // namespace pyre::grid


// order iterator operators
namespace pyre::grid {
    // equality
    template <class productT, class orderIteratorT, bool isConst>
    constexpr auto operator==(
        const OrderIterator<productT, orderIteratorT, isConst> &,
        const OrderIterator<productT, orderIteratorT, isConst> &) -> bool;
    // and not
    template <class productT, class orderIteratorT, bool isConst>
    constexpr auto operator!=(
        const OrderIterator<productT, orderIteratorT, isConst> &,
        const OrderIterator<productT, orderIteratorT, isConst> &) -> bool;
} // namespace pyre::grid


// index iterator operators
namespace pyre::grid {
    // equality
    template <class packingT>
    constexpr auto operator==(const IndexIterator<packingT> &, const IndexIterator<packingT> &)
        -> bool;
    // and not
    template <class packingT>
    constexpr auto operator!=(const IndexIterator<packingT> &, const IndexIterator<packingT> &)
        -> bool;
} // namespace pyre::grid


// grid iterator operators
namespace pyre::grid {
    // equality
    template <class gridT, class indexIteratorT, bool isConst>
    constexpr auto operator==(
        const GridIterator<gridT, indexIteratorT, isConst> &,
        const GridIterator<gridT, indexIteratorT, isConst> &) -> bool;
    // and not
    template <class gridT, class indexIteratorT, bool isConst>
    constexpr auto operator!=(
        const GridIterator<gridT, indexIteratorT, isConst> &,
        const GridIterator<gridT, indexIteratorT, isConst> &) -> bool;
} // namespace pyre::grid


// index algebra
namespace pyre::grid {
    // add a {shape} to an {index}
    template <class indexContainerT, class shapeContainerT>
    constexpr auto operator+(const Index<indexContainerT> &, const Shape<shapeContainerT> &)
        -> Index<indexContainerT>;
} // namespace pyre::grid


// structured binding support
// for indices
template <class containerT>
class std::tuple_size<pyre::grid::Index<containerT>>;

template <std::size_t I, class containerT>
struct std::tuple_element<I, pyre::grid::Index<containerT>>;


// for shapes
template <class containerT>
class std::tuple_size<pyre::grid::Shape<containerT>>;

template <std::size_t I, class containerT>
struct std::tuple_element<I, pyre::grid::Shape<containerT>>;


#endif

// end of file
