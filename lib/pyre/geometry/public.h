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
#include <pyre/memory.h>
#include <pyre/grid.h>

// forward declarations
namespace pyre {
    namespace geometry {
        // local type aliases
        typedef std::size_t size_t;
        // point
        template <size_t dim, typename dataT> class Point;
        // brick
        template <size_t dim, typename nodeT> class Brick;
    }
}

// type aliases for the above
namespace pyre {
    namespace geometry {
        // point
        template <size_t dim = 3, typename dataT = double>
        using point_t = Point<dim, dataT>;
        // brick
        template <size_t dim = 3, typename nodeT = point_t<3> >
        using brick_t = Brick<dim, nodeT>;

    }
}

// pull types from {pyre::grid}
namespace pyre {
    namespace geometry {
        template <typename repT>
        using index_t = pyre::grid::index_t<repT>;

        template <typename repT>
        using order_t = pyre::grid::order_t<repT>;

        template <typename indexT, typename orderT>
        using slice_t = pyre::grid::slice_t<indexT, orderT>;

        template <typename sliceT>
        using iterator_t = pyre::grid::iterator_t<sliceT>;

        template <typename indexT, typename orderT>
        using tile_t = pyre::grid::tile_t<indexT, orderT>;

        // grid
        template <typename cellT, typename tileT, typename storageT>
        using grid_t = pyre::grid::grid_t<cellT, tileT, storageT>;
        // direct grid
        template <typename cellT, typename tileT, typename directT = pyre::memory::direct_t>
        using directgrid_t = pyre::grid::directgrid_t<cellT, tileT, directT>;
    }
}

// operators
namespace pyre {
    namespace geometry {
        // operators on points
        // equality
        template <size_t dim, typename dataT>
        auto operator== (const Point<dim, dataT> & p1, const Point<dim, dataT> & p2);
        // inequality
        template <size_t dim, typename dataT>
        auto operator!= (const Point<dim, dataT> & p1, const Point<dim, dataT> & p2);

        // operators on bricks
        // equality
        template <size_t dim, typename nodeT>
        auto operator== (const Brick<dim, nodeT> & b1, const Brick<dim, nodeT> & b2);
        // inequality
        template <size_t dim, typename nodeT>
        auto operator!= (const Brick<dim, nodeT> & b1, const Brick<dim, nodeT> & b2);
    }
}


// stream injection: overload the global operator<<
// points
template <size_t dim, typename dataT>
auto & operator<< (std::ostream & stream, const pyre::geometry::Point<dim, dataT> & point);
// and bricks
template <size_t dim, typename nodeT>
auto & operator<< (std::ostream & stream, const pyre::geometry::Brick<dim, nodeT> & brick);


// the object model
#include "Point.h"
#include "Brick.h"

// the implementations
// point
#define pyre_geometry_Point_icc
#include "Point.icc"
#undef pyre_geometry_Point_icc

// brick
#define pyre_geometry_Brick_icc
#include "Brick.icc"
#undef pyre_geometry_Brick_icc

# endif

// end of file
