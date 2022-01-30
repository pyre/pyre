// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2022 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"

// my instantiations
#include "grids.h"


// wrappers over {pyre::grid::grid_t} template expansions
// build the submodule
void
pyre::py::grid::grids(py::module & m)
{
    // 2d const maps
    complexFloatConstMapGrid2D(m);
    // all done
    return;
}


// grid instantiations
void
pyre::py::grid::complexFloatConstMapGrid2D(py::module & m)
{
    // type aliases
    using cell_t = std::complex<float>;
    using layout_t = pyre::grid::canonical_t<2>;
    using storage_t = pyre::memory::constmap_t<cell_t>;
    using grid_t = pyre::grid::grid_t<layout_t, storage_t>;

    // build the class record
    auto cls = py::class_<grid_t>(
        // in scope
        m,
        // class name
        "ComplexFloatConstMapGrid2D",
        // docstring
        "a 2d grid backed by a read-only map of complex floats");

    // install the interface
    gridInterface(cls);

    // all done
    return;
}


// the interface decorator
template <class gridT>
void
pyre::py::grid::gridInterface(py::class_<gridT> & cls)
{
    // all done
    return;
}

// end of file
