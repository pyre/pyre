// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(h5_py_external_h)
#define h5_py_external_h


// STL
#include <algorithm>
#include <complex>
#include <memory>
#include <string>
// support
#include <pyre/h5.h>
#include <pyre/journal.h>
#include <pyre/memory.h>
#include <pyre/grid.h>
// pybind11
#include <pybind11/pybind11.h>
#include <pybind11/complex.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>
// hdf5
#include <H5Cpp.h>


// type aliases
namespace pyre::h5::py {
    // import {pybind11}
    namespace py = pybind11;
    // get the special {pybind11} literals
    using namespace py::literals;

    // for decorating pybind11 classes
    // class names
    using classname_t = const char *;
    // docstrings
    using docstring_t = const char *;

    // wrapper to install a {std::shared_ptr} as the custom holder for the bindings
    template <class classT>
    using shared_holder_t = py::class_<classT, std::shared_ptr<classT>>;

    // aliases for common STL classes
    using string_t = std::string;
    using names_t = std::vector<string_t>;
    using ints_t = std::vector<long>;
    using doubles_t = std::vector<double>;
    using strings_t = std::vector<string_t>;

    // for specifying dataspace coordinates and shapes
    using shape_t = std::vector<hsize_t>;
    using index_t = shape_t;
    using offsets_t = std::vector<hssize_t>;
    // a collection of dataspace coordinates
    using points_t = std::vector<shape_t>;

    // aliases of hdf5 entities
    // to avoid having to constantly look up which ones are prefixed by H5 and which not
    // structural entities
    using Identifier = H5::IdComponent; // pure virtual
    // property lists derive from {Identifier}
    using PropList = H5::PropList;
    using DAPL = H5::DSetAccPropList;
    using DCPL = H5::DSetCreatPropList;
    using DXPL = H5::DSetMemXferPropList;
    using FAPL = H5::FileAccPropList;
    using FCPL = H5::FileCreatPropList;
    using LAPL = H5::LinkAccPropList;
    using LCPL = H5::LinkCreatPropList;
    // dataspaces derive from {Identifier}
    using DataSpace = H5::DataSpace;
    // locations derive from {Identifier}
    using Location = H5::H5Location; // pure virtual
    // objects derive from {Location}
    using Object = H5::H5Object; // pure virtual
    // groups derive from {Object}
    using Group = H5::Group;
    using File = H5::H5File;
    // datasets derive from object
    using DataSet = H5::DataSet;
    // datatypes derive from {Object}
    using DataType = H5::DataType;
    using ArrayType = H5::ArrayType;   // derives DataType
    using AtomType = H5::AtomType;     // derives from DataType
    using FloatType = H5::FloatType;   // derives from AtomType
    using IntType = H5::IntType;       // derives from AtomType
    using PredType = H5::PredType;     // derives from AtomType
    using StrType = H5::StrType;       // derives from AtomType
    using CompType = H5::CompType;     // derives from DataType
    using EnumType = H5::EnumType;     // derives from DataType
    using VarLenType = H5::VarLenType; // derives from DataType

    // aliases for select memory template expansions
    using heap_int8_t = pyre::memory::heap_t<std::int8_t>;
    using heap_int16_t = pyre::memory::heap_t<std::int16_t>;
    using heap_int32_t = pyre::memory::heap_t<std::int32_t>;
    using heap_int64_t = pyre::memory::heap_t<std::int64_t>;
    using heap_uint8_t = pyre::memory::heap_t<std::uint8_t>;
    using heap_uint16_t = pyre::memory::heap_t<std::uint16_t>;
    using heap_uint32_t = pyre::memory::heap_t<std::uint32_t>;
    using heap_uint64_t = pyre::memory::heap_t<std::uint64_t>;
    using heap_float_t = pyre::memory::heap_t<float>;
    using heap_double_t = pyre::memory::heap_t<double>;
    using heap_complexfloat_t = pyre::memory::heap_t<std::complex<float>>;
    using heap_complexdouble_t = pyre::memory::heap_t<std::complex<double>>;

    using int8_heapgrid_2d_t =
        pyre::grid::grid_t<pyre::grid::canonical_t<2>, pyre::memory::heap_t<int8_t>>;
    using int16_heapgrid_2d_t =
        pyre::grid::grid_t<pyre::grid::canonical_t<2>, pyre::memory::heap_t<int16_t>>;
    using int32_heapgrid_2d_t =
        pyre::grid::grid_t<pyre::grid::canonical_t<2>, pyre::memory::heap_t<int32_t>>;
    using int64_heapgrid_2d_t =
        pyre::grid::grid_t<pyre::grid::canonical_t<2>, pyre::memory::heap_t<int64_t>>;
    using uint8_heapgrid_2d_t =
        pyre::grid::grid_t<pyre::grid::canonical_t<2>, pyre::memory::heap_t<uint8_t>>;
    using uint16_heapgrid_2d_t =
        pyre::grid::grid_t<pyre::grid::canonical_t<2>, pyre::memory::heap_t<uint16_t>>;
    using uint32_heapgrid_2d_t =
        pyre::grid::grid_t<pyre::grid::canonical_t<2>, pyre::memory::heap_t<uint32_t>>;
    using uint64_heapgrid_2d_t =
        pyre::grid::grid_t<pyre::grid::canonical_t<2>, pyre::memory::heap_t<uint64_t>>;
    using float_heapgrid_2d_t =
        pyre::grid::grid_t<pyre::grid::canonical_t<2>, pyre::memory::heap_t<float>>;
    using double_heapgrid_2d_t =
        pyre::grid::grid_t<pyre::grid::canonical_t<2>, pyre::memory::heap_t<double>>;
    using complexfloat_heapgrid_2d_t =
        pyre::grid::grid_t<pyre::grid::canonical_t<2>, pyre::memory::heap_t<std::complex<float>>>;
    using complexdouble_heapgrid_2d_t =
        pyre::grid::grid_t<pyre::grid::canonical_t<2>, pyre::memory::heap_t<std::complex<double>>>;

} // namespace pyre::h5::py


#endif

// end of file
