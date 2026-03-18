// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"
// my instantiations
#include "grids.h"

// forward declarations of the per-dimension binders
namespace pyre::py::grid {
    void grids_1d(py::module &);
    void grids_2d(py::module &);
    void grids_3d(py::module &);
    void grids_4d(py::module &);
}

void
pyre::py::grid::grids(py::module & m)
{
    // populate the typename table
    // heap
    typenames[std::type_index(typeid(heap_char_t))] = "CharHeap";
    // signed integral types
    typenames[std::type_index(typeid(heap_int8_t))] = "Int8Heap";
    typenames[std::type_index(typeid(heap_int16_t))] = "Int16Heap";
    typenames[std::type_index(typeid(heap_int32_t))] = "Int32Heap";
    typenames[std::type_index(typeid(heap_int64_t))] = "Int64Heap";
    // unsigned integral types
    typenames[std::type_index(typeid(heap_uint8_t))] = "UInt8Heap";
    typenames[std::type_index(typeid(heap_uint16_t))] = "UInt16Heap";
    typenames[std::type_index(typeid(heap_uint32_t))] = "UInt32Heap";
    typenames[std::type_index(typeid(heap_uint64_t))] = "UInt64Heap";
    // floating point types
    typenames[std::type_index(typeid(heap_float_t))] = "FloatHeap";
    typenames[std::type_index(typeid(heap_double_t))] = "DoubleHeap";
    // complex types
    typenames[std::type_index(typeid(heap_complexfloat_t))] = "ComplexFloatHeap";
    typenames[std::type_index(typeid(heap_complexdouble_t))] = "ComplexDoubleHeap";

    // constheap
    typenames[std::type_index(typeid(constheap_char_t))] = "CharConstHeap";
    // signed integral types
    typenames[std::type_index(typeid(constheap_int8_t))] = "Int8ConstHeap";
    typenames[std::type_index(typeid(constheap_int16_t))] = "Int16ConstHeap";
    typenames[std::type_index(typeid(constheap_int32_t))] = "Int32ConstHeap";
    typenames[std::type_index(typeid(constheap_int64_t))] = "Int64ConstHeap";
    // unsigned integral types
    typenames[std::type_index(typeid(constheap_uint8_t))] = "UInt8ConstHeap";
    typenames[std::type_index(typeid(constheap_uint16_t))] = "UInt16ConstHeap";
    typenames[std::type_index(typeid(constheap_uint32_t))] = "UInt32ConstHeap";
    typenames[std::type_index(typeid(constheap_uint64_t))] = "UInt64ConstHeap";
    // floating point types
    typenames[std::type_index(typeid(constheap_float_t))] = "FloatConstHeap";
    typenames[std::type_index(typeid(constheap_double_t))] = "DoubleConstHeap";
    // complex types
    typenames[std::type_index(typeid(constheap_complexfloat_t))] = "ComplexFloatConstHeap";
    typenames[std::type_index(typeid(constheap_complexdouble_t))] = "ComplexDoubleConstHeap";

    // map
    typenames[std::type_index(typeid(map_char_t))] = "CharMap";
    // signed integral types
    typenames[std::type_index(typeid(map_int8_t))] = "Int8Map";
    typenames[std::type_index(typeid(map_int16_t))] = "Int16Map";
    typenames[std::type_index(typeid(map_int32_t))] = "Int32Map";
    typenames[std::type_index(typeid(map_int64_t))] = "Int64Map";
    // unsigned integral types
    typenames[std::type_index(typeid(map_uint8_t))] = "UInt8Map";
    typenames[std::type_index(typeid(map_uint16_t))] = "UInt16Map";
    typenames[std::type_index(typeid(map_uint32_t))] = "UInt32Map";
    typenames[std::type_index(typeid(map_uint64_t))] = "UInt64Map";
    // floating point types
    typenames[std::type_index(typeid(map_float_t))] = "FloatMap";
    typenames[std::type_index(typeid(map_double_t))] = "DoubleMap";
    // complex types
    typenames[std::type_index(typeid(map_complexfloat_t))] = "ComplexFloatMap";
    typenames[std::type_index(typeid(map_complexdouble_t))] = "ComplexDoubleMap";

    // constmap
    typenames[std::type_index(typeid(constmap_char_t))] = "CharConstMap";
    // signed integral types
    typenames[std::type_index(typeid(constmap_int8_t))] = "Int8ConstMap";
    typenames[std::type_index(typeid(constmap_int16_t))] = "Int16ConstMap";
    typenames[std::type_index(typeid(constmap_int32_t))] = "Int32ConstMap";
    typenames[std::type_index(typeid(constmap_int64_t))] = "Int64ConstMap";
    // unsigned integral types
    typenames[std::type_index(typeid(constmap_uint8_t))] = "UInt8ConstMap";
    typenames[std::type_index(typeid(constmap_uint16_t))] = "UInt16ConstMap";
    typenames[std::type_index(typeid(constmap_uint32_t))] = "UInt32ConstMap";
    typenames[std::type_index(typeid(constmap_uint64_t))] = "UInt64ConstMap";
    // floating point types
    typenames[std::type_index(typeid(constmap_float_t))] = "FloatConstMap";
    typenames[std::type_index(typeid(constmap_double_t))] = "DoubleConstMap";
    // complex types
    typenames[std::type_index(typeid(constmap_complexfloat_t))] = "ComplexFloatConstMap";
    typenames[std::type_index(typeid(constmap_complexdouble_t))] = "ComplexDoubleConstMap";

    // view
    typenames[std::type_index(typeid(view_char_t))] = "CharView";
    // signed integral types
    typenames[std::type_index(typeid(view_int8_t))] = "Int8View";
    typenames[std::type_index(typeid(view_int16_t))] = "Int16View";
    typenames[std::type_index(typeid(view_int32_t))] = "Int32View";
    typenames[std::type_index(typeid(view_int64_t))] = "Int64View";
    // unsigned integral types
    typenames[std::type_index(typeid(view_uint8_t))] = "UInt8View";
    typenames[std::type_index(typeid(view_uint16_t))] = "UInt16View";
    typenames[std::type_index(typeid(view_uint32_t))] = "UInt32View";
    typenames[std::type_index(typeid(view_uint64_t))] = "UInt64View";
    // floating point types
    typenames[std::type_index(typeid(view_float_t))] = "FloatView";
    typenames[std::type_index(typeid(view_double_t))] = "DoubleView";
    // complex types
    typenames[std::type_index(typeid(view_complexfloat_t))] = "ComplexFloatView";
    typenames[std::type_index(typeid(view_complexdouble_t))] = "ComplexDoubleView";

    // constmap
    typenames[std::type_index(typeid(constview_char_t))] = "CharConstView";
    // signed integral types
    typenames[std::type_index(typeid(constview_int8_t))] = "Int8ConstView";
    typenames[std::type_index(typeid(constview_int16_t))] = "Int16ConstView";
    typenames[std::type_index(typeid(constview_int32_t))] = "Int32ConstView";
    typenames[std::type_index(typeid(constview_int64_t))] = "Int64ConstView";
    // unsigned integral types
    typenames[std::type_index(typeid(constview_uint8_t))] = "UInt8ConstView";
    typenames[std::type_index(typeid(constview_uint16_t))] = "UInt16ConstView";
    typenames[std::type_index(typeid(constview_uint32_t))] = "UInt32ConstView";
    typenames[std::type_index(typeid(constview_uint64_t))] = "UInt64ConstView";
    // floating point types
    typenames[std::type_index(typeid(constview_float_t))] = "FloatConstView";
    typenames[std::type_index(typeid(constview_double_t))] = "DoubleConstView";
    // complex types
    typenames[std::type_index(typeid(constview_complexfloat_t))] = "ComplexFloatConstView";
    typenames[std::type_index(typeid(constview_complexdouble_t))] = "ComplexDoubleConstView";

    // build the class records per dimension
    grids_1d(m);
    grids_2d(m);
    grids_3d(m);
    grids_4d(m);

    // all done
    return;
}


// end of file
