// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2018 all rights reserved
//

// code guard
#if !defined(pyre_grid_public_h)
#define pyre_grid_public_h

// externals
#include <stdexcept>
#include <array>
// support
#include <pyre/journal.h>
#include <pyre/memory.h>

// forward declarations
namespace pyre {
    namespace grid {
        // local type aliases
        // for describing shapes and regions
        typedef std::size_t size_t;
        // indices
        template <typename repT> class Index;
        // index ordering
        template <size_t dim> class Packing;
        // slices
        template <typename indexT, typename packingT> class Slice;
        // iterators over index ranges
        template <typename sliceT> class Iterator;
        // layouts
        template <typename indexT, typename packingT> class Layout;

        // grid
        template <typename cellT, typename layoutT, typename storageT> class Grid;
        // direct grid: a memory mapped grid
        template <typename cellT, typename layoutT, typename directT> class DirectGrid;
    }
}

// type aliases for the above; these are the type names that form the public interface of this
// package; please consider anything else in this file as an implementation detail
namespace pyre {
    namespace grid {
        template <typename repT> using index_t = Index<repT>;
        template <typename repT> using shape_t = Index<repT>;
        template <size_t dim> using packing_t = Packing<dim>;

        template <typename indexT, typename packingT = Packing<indexT::dim()>>
        using slice_t = Slice<indexT, packingT>;

        template <typename sliceT> using iterator_t = Iterator<sliceT>;

        template <typename indexT, typename packingT = Packing<indexT::dim()>>
        using layout_t = Layout<indexT, packingT>;

        // grid
        template <typename cellT, typename layoutT, typename storageT>
        using grid_t = Grid<cellT, layoutT, storageT>;

        // direct grid
        template < typename cellT,
                   typename layoutT,
                   typename directT = pyre::memory::direct_t<cellT>>
        using directgrid_t = DirectGrid<cellT, layoutT, directT>;

        // simplified access
        template < size_t dim,
                   typename cellT = double,
                   typename repT = std::array<int, dim>,
                   typename storageT = pyre::memory::heap_t<cellT>>
        using simple_t = Grid<cellT, Layout<Index<repT>, Packing<dim>>, storageT>;
    }
}

// operators
namespace pyre {
    namespace grid {
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

        // stream injection: overload the global operator<<
        // for indices
        template <typename repT>
        auto & operator<< (std::ostream & stream, const Index<repT> & index);
        // packing strategies
        template <size_t dim>
        auto & operator<< (std::ostream & stream, const Packing<dim> & packing);
        // layouts
        template <typename indexT, typename packingT>
        auto & operator<< (std::ostream & stream, const Layout<indexT, packingT> & layout);

    }
}


// the object model
#include "Packing.h"
#include "Index.h"
#include "Slice.h"
#include "Iterator.h"
#include "Layout.h"
#include "Grid.h"
#include "DirectGrid.h"

// the implementations
// packing
#define pyre_grid_Packing_icc
#include "Packing.icc"
#undef pyre_grid_Packing_icc

// index
#define pyre_grid_Index_icc
#include "Index.icc"
#undef pyre_grid_Index_icc

// slice
#define pyre_grid_Slice_icc
#include "Slice.icc"
#undef pyre_grid_Slice_icc

// iterator
#define pyre_grid_Iterator_icc
#include "Iterator.icc"
#undef pyre_grid_Iterator_icc

// layout
#define pyre_grid_Layout_icc
#include "Layout.icc"
#undef pyre_grid_Layout_icc

// grid
#define pyre_grid_Grid_icc
#include "Grid.icc"
#undef pyre_grid_Grid_icc

// grid
#define pyre_grid_DirectGrid_icc
#include "DirectGrid.icc"
#undef pyre_grid_DirectGrid_icc

# endif

// end of file
