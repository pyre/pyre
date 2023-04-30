// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2023 all rights reserved
//

// code guard
#if !defined(pyre_geometry_public_h)
#define pyre_geometry_public_h

// externals
#include <stdexcept>
#include <array>
#include <valarray>
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
        // point cloud
        template <typename pointT> class PointCloud;
        // brick
        template <size_t dim, typename nodeT> class Brick;
    }
}

// type aliases for the above
namespace pyre {
    namespace geometry {
        // point
        template <size_t dim = 3, typename dataT = double> using point_t = Point<dim, dataT>;
        // point cloud
        template <typename pointT = point_t<3, double>> using cloud_t = PointCloud<pointT>;
        // brick
        template <size_t dim = 3, typename nodeT = point_t<3> > using brick_t = Brick<dim, nodeT>;
    }
}

// operators
namespace pyre {
    namespace geometry {
        // operators on points
        // equality
        template <size_t dim, typename dataT>
        inline
        auto operator== (const Point<dim, dataT> & p1, const Point<dim, dataT> & p2);
        // inequality
        template <size_t dim, typename dataT>
        inline
        auto operator!= (const Point<dim, dataT> & p1, const Point<dim, dataT> & p2);

        // operators on bricks
        // equality
        template <size_t dim, typename nodeT>
        inline
        auto operator== (const Brick<dim, nodeT> & b1, const Brick<dim, nodeT> & b2);
        // inequality
        template <size_t dim, typename nodeT>
        inline
        auto operator!= (const Brick<dim, nodeT> & b1, const Brick<dim, nodeT> & b2);

        // stream injection: overload the global operator<<
        // points
        template <size_t dim, typename dataT>
        inline
        auto & operator<< (std::ostream & stream, const Point<dim, dataT> & point);
        // bricks
        template <size_t dim, typename nodeT>
        inline
        auto & operator<< (std::ostream & stream, const Brick<dim, nodeT> & brick);
    }
}


// the object model
#include "Point.h"
#include "PointCloud.h"
#include "Brick.h"

// the implementations
// point
#define pyre_geometry_Point_icc
#include "Point.icc"
#undef pyre_geometry_Point_icc

// point cloud
#define pyre_geometry_PointCloud_icc
#include "PointCloud.icc"
#undef pyre_geometry_PointCloud_icc

// brick
#define pyre_geometry_Brick_icc
#include "Brick.icc"
#undef pyre_geometry_Brick_icc

# endif

// end of file
