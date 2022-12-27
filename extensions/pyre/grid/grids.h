// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_py_grid_grids_h)
#define pyre_py_grid_grids_h


// the {pyre} extension namespace
namespace pyre::py::grid {
    // the grid instantiations
    // 2d
    void byteConstMapGrid2D(py::module &);
    void int16ConstMapGrid2D(py::module &);
    void int32ConstMapGrid2D(py::module &);
    void int64ConstMapGrid2D(py::module &);
    void floatConstMapGrid2D(py::module &);
    void doubleConstMapGrid2D(py::module &);
    void complexFloatConstMapGrid2D(py::module &);
    void complexDoubleConstMapGrid2D(py::module &);
    // 3d
    void byteConstMapGrid3D(py::module &);
    void int16ConstMapGrid3D(py::module &);
    void int32ConstMapGrid3D(py::module &);
    void int64ConstMapGrid3D(py::module &);
    void floatConstMapGrid3D(py::module &);
    void doubleConstMapGrid3D(py::module &);
    void complexFloatConstMapGrid3D(py::module &);
    void complexDoubleConstMapGrid3D(py::module &);
    // 4d
    void byteConstMapGrid4D(py::module &);
    void int16ConstMapGrid4D(py::module &);
    void int32ConstMapGrid4D(py::module &);
    void int64ConstMapGrid4D(py::module &);
    void floatConstMapGrid4D(py::module &);
    void doubleConstMapGrid4D(py::module &);
    void complexFloatConstMapGrid4D(py::module &);
    void complexDoubleConstMapGrid4D(py::module &);

    // the interface decorators
    template <class gridT>
    void constmapInterface(py::class_<gridT> &);

    template <class gridT>
    void mapInterface(py::class_<gridT> &);

    template <class gridT>
    void constgridInterface(py::class_<gridT> &);

    template <class gridT>
    void gridInterface(py::class_<gridT> &);

} // namespace pyre::py::grid


#endif

// end of file
