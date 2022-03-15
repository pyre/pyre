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
    byteConstMapGrid2D(m);
    int16ConstMapGrid2D(m);
    int32ConstMapGrid2D(m);
    int64ConstMapGrid2D(m);
    floatConstMapGrid2D(m);
    doubleConstMapGrid2D(m);
    complexFloatConstMapGrid2D(m);
    complexDoubleConstMapGrid2D(m);
    // all done
    return;
}


// grid instantiations
void
pyre::py::grid::byteConstMapGrid2D(py::module & m)
{
    // type aliases
    using cell_t = char;
    using packing_t = pyre::grid::canonical_t<2>;
    using storage_t = pyre::memory::constmap_t<cell_t>;
    using grid_t = pyre::grid::grid_t<packing_t, storage_t>;

    // build the class record
    auto cls = py::class_<grid_t>(
        // in scope
        m,
        // class name
        "ByteConstMapGrid2D",
        // docstring
        "a 2d grid backed by a read-only map of bytes");

    // the map specific interface
    constmapInterface(cls);
    // the grid interface
    constgridInterface(cls);

    // all done
    return;
}


void
pyre::py::grid::int16ConstMapGrid2D(py::module & m)
{
    // type aliases
    using cell_t = int16_t;
    using packing_t = pyre::grid::canonical_t<2>;
    using storage_t = pyre::memory::constmap_t<cell_t>;
    using grid_t = pyre::grid::grid_t<packing_t, storage_t>;

    // build the class record
    auto cls = py::class_<grid_t>(
        // in scope
        m,
        // class name
        "Int16ConstMapGrid2D",
        // docstring
        "a 2d grid backed by a read-only map of {int16_t}");

    // the map specific interface
    constmapInterface(cls);
    // the grid interface
    constgridInterface(cls);

    // all done
    return;
}


void
pyre::py::grid::int32ConstMapGrid2D(py::module & m)
{
    // type aliases
    using cell_t = int32_t;
    using packing_t = pyre::grid::canonical_t<2>;
    using storage_t = pyre::memory::constmap_t<cell_t>;
    using grid_t = pyre::grid::grid_t<packing_t, storage_t>;

    // build the class record
    auto cls = py::class_<grid_t>(
        // in scope
        m,
        // class name
        "Int32ConstMapGrid2D",
        // docstring
        "a 2d grid backed by a read-only map of {int32_t}");

    // the map specific interface
    constmapInterface(cls);
    // the grid interface
    constgridInterface(cls);

    // all done
    return;
}


void
pyre::py::grid::int64ConstMapGrid2D(py::module & m)
{
    // type aliases
    using cell_t = int64_t;
    using packing_t = pyre::grid::canonical_t<2>;
    using storage_t = pyre::memory::constmap_t<cell_t>;
    using grid_t = pyre::grid::grid_t<packing_t, storage_t>;

    // build the class record
    auto cls = py::class_<grid_t>(
        // in scope
        m,
        // class name
        "Int64ConstMapGrid2D",
        // docstring
        "a 2d grid backed by a read-only map of {int64_t}");

    // the map specific interface
    constmapInterface(cls);
    // the grid interface
    constgridInterface(cls);

    // all done
    return;
}


void
pyre::py::grid::floatConstMapGrid2D(py::module & m)
{
    // type aliases
    using cell_t = float;
    using packing_t = pyre::grid::canonical_t<2>;
    using storage_t = pyre::memory::constmap_t<cell_t>;
    using grid_t = pyre::grid::grid_t<packing_t, storage_t>;

    // build the class record
    auto cls = py::class_<grid_t>(
        // in scope
        m,
        // class name
        "FloatConstMapGrid2D",
        // docstring
        "a 2d grid backed by a read-only map of floats");

    // the map specific interface
    constmapInterface(cls);
    // the grid interface
    constgridInterface(cls);

    // all done
    return;
}


void
pyre::py::grid::doubleConstMapGrid2D(py::module & m)
{
    // type aliases
    using cell_t = double;
    using packing_t = pyre::grid::canonical_t<2>;
    using storage_t = pyre::memory::constmap_t<cell_t>;
    using grid_t = pyre::grid::grid_t<packing_t, storage_t>;

    // build the class record
    auto cls = py::class_<grid_t>(
        // in scope
        m,
        // class name
        "DoubleConstMapGrid2D",
        // docstring
        "a 2d grid backed by a read-only map of doubles");

    // the map specific interface
    constmapInterface(cls);
    // the grid interface
    constgridInterface(cls);

    // all done
    return;
}


void
pyre::py::grid::complexFloatConstMapGrid2D(py::module & m)
{
    // type aliases
    using cell_t = std::complex<float>;
    using packing_t = pyre::grid::canonical_t<2>;
    using storage_t = pyre::memory::constmap_t<cell_t>;
    using grid_t = pyre::grid::grid_t<packing_t, storage_t>;

    // build the class record
    auto cls = py::class_<grid_t>(
        // in scope
        m,
        // class name
        "ComplexFloatConstMapGrid2D",
        // docstring
        "a 2d grid backed by a read-only map of complex floats");

    // the map specific interface
    constmapInterface(cls);
    // the grid interface
    constgridInterface(cls);

    // all done
    return;
}


void
pyre::py::grid::complexDoubleConstMapGrid2D(py::module & m)
{
    // type aliases
    using cell_t = std::complex<double>;
    using packing_t = pyre::grid::canonical_t<2>;
    using storage_t = pyre::memory::constmap_t<cell_t>;
    using grid_t = pyre::grid::grid_t<packing_t, storage_t>;

    // build the class record
    auto cls = py::class_<grid_t>(
        // in scope
        m,
        // class name
        "ComplexDoubleConstMapGrid2D",
        // docstring
        "a 2d grid backed by a read-only map of complex doubles");

    // the map specific interface
    constmapInterface(cls);
    // the grid interface
    constgridInterface(cls);

    // all done
    return;
}


// the map specific constructors
template <class gridT>
void
pyre::py::grid::constmapInterface(py::class_<gridT> & cls)
{
    // constructors
    cls.def(
        // the implementation
        py::init<typename gridT::packing_const_reference, typename gridT::storage_pointer>(),
        //
        "packing"_a, "storage"_a,
        // the docstring
        "make a new grid over the {storage} with the given {packing} strategy");

    // all done
    return;
}


// the const grid interface decorator
template <class gridT>
void
pyre::py::grid::constgridInterface(py::class_<gridT> & cls)
{
    // accessors
    // layout
    cls.def_property_readonly(
        // the name of the method
        "layout",
        // the implementation
        &gridT::layout,
        // the docstring
        "access my layout");

    // data access
    // by index
    cls.def(
        // the name of the method
        "__getitem__",
        // the implementation
        [](const gridT & self, typename gridT::index_const_reference index) {
            // get the value at the given {index}
            return self.at(index);
        },
        // the signature
        "index"_a,
        // the docstring
        "get the value at the specified {index}");

    // by offset
    cls.def(
        // the name of the method
        "__getitem__",
        // the implementation
        [](const gridT & self, typename gridT::difference_type offset) {
            // get the value at the given {offset}
            return self.at(offset);
        },
        // the signature
        "offset"_a,
        // the docstring
        "get the value at the specified {offset}");

    // all done
    return;
}


// the grid interface decorator
template <class gridT>
void
pyre::py::grid::gridInterface(py::class_<gridT> & cls)
{
    // data access
    // by index
    cls.def(
        // the name of the method
        "__setitem__",
        // the implementation
        [](const gridT & self, typename gridT::index_const_reference index,
           typename gridT::value_type value) -> void {
            // set the value at the given {index}
            self.at(index) = value;
            // all done
        },
        // the signature
        "index"_a,
        // the docstring
        "get the value at the specified {index}");

    // by offset
    cls.def(
        // the name of the method
        "__setitem__",
        // the implementation
        [](const gridT & self, typename gridT::difference_type offset,
           typename gridT::value_type value) -> void {
            // set the value at the given {offset}
            self.at(offset) = value;
            // all done
            return;
        },
        // the signature
        "offset"_a,
        // the docstring
        "get the value at the specified {offset}");

    // all done
    return;
}


// end of file
