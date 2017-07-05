// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2017 all rights reserved
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
        template <typename repT> class Packing;
        // slices
        template <typename indexT, typename packingT> class Slice;
        // iterators over index ranges
        template <typename sliceT> class Iterator;
        // tiles
        template <typename indexT, typename packingT> class Tile;

        // grid
        template <typename cellT, typename tileT, typename storageT> class Grid;
        // direct grid: a memory mapped grid
        template <typename cellT, typename tileT, typename directT> class DirectGrid;
    }
}

// type aliases for the above
namespace pyre {
    namespace grid {
        template <typename repT> using index_t = Index<repT>;
        template <typename repT> using packing_t = Packing<repT>;

        template <typename indexT, typename packingT> using slice_t = Slice<indexT, packingT>;

        template <typename sliceT> using iterator_t = Iterator<sliceT>;

        template <typename indexT, typename packingT> using tile_t = Tile<indexT, packingT>;

        // grid
        template <typename cellT, typename tileT, typename storageT>
        using grid_t = Grid<cellT, tileT, storageT>;
        // direct grid
        template <typename cellT, typename tileT, typename directT = pyre::memory::direct_t>
        using directgrid_t = DirectGrid<cellT, tileT, directT>;
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
    }
}


// stream injection: overload the global operator<<
// for indices
template <typename repT>
auto & operator<< (std::ostream & stream, const pyre::grid::Index<repT> & index);
// packing strategies
template <typename repT>
auto & operator<< (std::ostream & stream, const pyre::grid::Packing<repT> & packing);
// tiles
template <typename indexT, typename packingT>
auto & operator<< (std::ostream & stream, const pyre::grid::Tile<indexT, packingT> & tile);

// the object model
#include "Packing.h"
#include "Index.h"
#include "Slice.h"
#include "Iterator.h"
#include "Tile.h"
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

// tile
#define pyre_grid_Tile_icc
#include "Tile.icc"
#undef pyre_grid_Tile_icc

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
