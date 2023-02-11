// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(h5_py_external_h)
#define h5_py_external_h


// STL
#include <algorithm>
#include <memory>
#include <string>
// support
#include <pyre/journal.h>
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
    using ints_t = std::vector<long>;
    using doubles_t = std::vector<double>;
    using strings_t = std::vector<string_t>;

    // for specifying dataspace coordinates and shapes
    using dims_t = std::vector<hsize_t>;
    using offsets_t = std::vector<hssize_t>;
    // a collection of dataspace coordinates
    using points_t = std::vector<dims_t>;

    // aliases of hdf5 entities
    // to avoid having to constantly look up which ones are prefixed by H5 and which not
    // structural entities
    using Identifier = H5::IdComponent; // pure virtual
    // property lists derive from {Identifier}
    using PropList = H5::PropList;
    using FileAccessPropertyList = H5::FileAccPropList;
    using FileCreatePropertyList = H5::FileCreatPropList;
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

} // namespace pyre::h5::py


#endif

// end of file
