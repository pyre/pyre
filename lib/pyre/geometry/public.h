// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2016 all rights reserved
//

// code guard
#if !defined(pyre_geometry_public_h)
#define pyre_geometry_public_h

// externals
#include <stdexcept>
#include <array>
// support
#include <pyre/journal.h>

// forward declarations
namespace pyre {
    namespace geometry {
        // local type aliases
        // for describing shapes and regions
        typedef std::size_t size_t;
        // indices
        template <typename repT> class Index;
        // index ordering
        template <typename repT> class Order;
        // slices
        template <typename indexT, typename orderT> class Slice;
        // iterators over index ranges
        template <typename sliceT> class Iterator;
        // tiles
        template <typename indexT, typename orderT> class Tile;

        // point
        template <size_t dim, typename dataT> class Point;
        // brick
        template <size_t dim, typename nodeT> class Brick;
        // corner point grid
        template <typename cellT, typename tileT, typename storageT> class Grid;
    }
}

// type aliases for the above
namespace pyre {
    namespace geometry {
        template <typename repT> using index_t = Index<repT>;
        template <typename repT> using order_t = Order<repT>;

        template <typename indexT, typename orderT> using slice_t = Slice<indexT, orderT>;

        template <typename sliceT> using iterator_t = Iterator<sliceT>;

        template <typename indexT, typename orderT> using tile_t = Tile<indexT, orderT>;

        // point
        template <std::size_t dim = 3, typename dataT = double>
        using point_t = Point<dim, dataT>;
        // brick
        template <std::size_t dim = 3, typename nodeT = point_t<3> >
        using brick_t = Brick<dim, nodeT>;
        // corner point grid
        template <typename cellT, typename tileT, typename storageT>
        using grid_t = Grid<cellT, tileT, storageT>;
    }
}

// operators
namespace pyre {
    namespace geometry {
        // operators on indices
        // equality
        template <typename repT>
        auto operator== (const Index<repT> &, const Index<repT> &);
        // inequality
        template <typename repT>
        auto operator!= (const Index<repT> &, const Index<repT> &);

        // operators on iterators
        // equality
        template <typename sliceT>
        auto operator== (const Iterator<sliceT> &, const Iterator<sliceT> &);
        // inequality
        template <typename sliceT>
        auto operator!= (const Iterator<sliceT> &, const Iterator<sliceT> &);

        // operators on points
        // equality
        template <std::size_t dim, typename dataT>
        auto operator== (const Point<dim, dataT> & p1, const Point<dim, dataT> & p2);
        // inequality
        template <std::size_t dim, typename dataT>
        auto operator!= (const Point<dim, dataT> & p1, const Point<dim, dataT> & p2);

        // operators on bricks
        // equality
        template <std::size_t dim, typename nodeT>
        auto operator== (const Brick<dim, nodeT> & b1, const Brick<dim, nodeT> & b2);
        // inequality
        template <std::size_t dim, typename nodeT>
        auto operator!= (const Brick<dim, nodeT> & b1, const Brick<dim, nodeT> & b2);
    }
}


// stream injection: overload the global operator<<
// for indices
template <typename repT>
auto & operator<< (std::ostream & stream, const pyre::geometry::Index<repT> & index);
// orders
template <typename repT>
auto & operator<< (std::ostream & stream, const pyre::geometry::Order<repT> & order);
// points
template <std::size_t dim, typename dataT>
auto & operator<< (std::ostream & stream, const pyre::geometry::Point<dim, dataT> & point);
// and bricks
template <std::size_t dim, typename nodeT>
auto & operator<< (std::ostream & stream, const pyre::geometry::Brick<dim, nodeT> & brick);


// the object model
#include "Order.h"
#include "Index.h"
#include "Slice.h"
#include "Iterator.h"
#include "Tile.h"
#include "Point.h"
#include "Brick.h"
#include "Grid.h"

// the implementations
// order
#define pyre_geometry_Order_icc
#include "Order.icc"
#undef pyre_geometry_Order_icc

// index
#define pyre_geometry_Index_icc
#include "Index.icc"
#undef pyre_geometry_Index_icc

// slice
#define pyre_geometry_Slice_icc
#include "Slice.icc"
#undef pyre_geometry_Slice_icc

// iterator
#define pyre_geometry_Iterator_icc
#include "Iterator.icc"
#undef pyre_geometry_Iterator_icc

// tile
#define pyre_geometry_Tile_icc
#include "Tile.icc"
#undef pyre_geometry_Tile_icc

// point
#define pyre_geometry_Point_icc
#include "Point.icc"
#undef pyre_geometry_Point_icc

// brick
#define pyre_geometry_Brick_icc
#include "Brick.icc"
#undef pyre_geometry_Brick_icc

// corner point grid
#define pyre_geometry_Grid_icc
#include "Grid.icc"
#undef pyre_geometry_Grid_icc
#endif


// end of file
