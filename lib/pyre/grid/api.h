// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_grid_api_h)
#define pyre_grid_api_h


// low level entities; you should probably stay away from them
namespace pyre::grid {
    // this wrapper over a {std::array}-like container
    // thin adaptor over a compile time container
    template <typename T, int N, template <typename, std::size_t> class containerT = std::array>
    using rep_t = Rep<containerT<T, N>>;

    // support for the multidimensional objects in this package
    template <
        int N, typename T = int, template <typename, std::size_t> class containerT = std::array>
    using product_t = Product<containerT<T, N>>;

    // the number of possible values of each axis
    template <
        int N, typename T = int, template <typename, std::size_t> class containerT = std::array>
    using shape_t = Shape<containerT<T, N>>;

    // indices
    template <
        int N, typename T = int, template <typename, std::size_t> class containerT = std::array>
    using index_t = Index<containerT<T, N>>;

    // the order in which indices are packed in memory
    template <
        int N, typename T = int, template <typename, std::size_t> class containerT = std::array>
    using order_t = Order<containerT<T, N>>;

    // in order product rank traversal
    template <class productT, class orderIteratorT, bool isConst = true>
    using order_iterator_t = OrderIterator<productT, orderIteratorT, isConst>;

    // ordered index generator
    template <class packingT>
    using index_iterator_t = IndexIterator<packingT>;
    // the canonical packing strategy
    template <int N, template <typename, std::size_t> class containerT = std::array>
    using canonical_t = Canonical<N, containerT>;

    // the grid
    template <class packingT, class storageT>
    using grid_t = Grid<packingT, storageT>;
    // and its iterator
    template <class gridT, class indexIteratorT, bool isConst>
    using grid_iterator_t = GridIterator<gridT, indexIteratorT, isConst>;
} // namespace pyre::grid


#endif

// end of file
