// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"

// my instantiations
#include "grids.h"

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

    // build the class records
    // 2d grids
    // heap
    bind<heap_char_t, 2>(m);
    bind<heap_int8_t, 2>(m);
    bind<heap_int16_t, 2>(m);
    bind<heap_int32_t, 2>(m);
    bind<heap_int64_t, 2>(m);
    bind<heap_uint8_t, 2>(m);
    bind<heap_uint16_t, 2>(m);
    bind<heap_uint32_t, 2>(m);
    bind<heap_uint64_t, 2>(m);
    bind<heap_float_t, 2>(m);
    bind<heap_double_t, 2>(m);
    bind<heap_complexfloat_t, 2>(m);
    bind<heap_complexdouble_t, 2>(m);
    // constheap
    bindconst<constheap_char_t, 2>(m);
    bindconst<constheap_int8_t, 2>(m);
    bindconst<constheap_int16_t, 2>(m);
    bindconst<constheap_int32_t, 2>(m);
    bindconst<constheap_int64_t, 2>(m);
    bindconst<constheap_uint8_t, 2>(m);
    bindconst<constheap_uint16_t, 2>(m);
    bindconst<constheap_uint32_t, 2>(m);
    bindconst<constheap_uint64_t, 2>(m);
    bindconst<constheap_float_t, 2>(m);
    bindconst<constheap_double_t, 2>(m);
    bindconst<constheap_complexfloat_t, 2>(m);
    bindconst<constheap_complexdouble_t, 2>(m);
    // map
    bind<map_char_t, 2>(m);
    bind<map_int8_t, 2>(m);
    bind<map_int16_t, 2>(m);
    bind<map_int32_t, 2>(m);
    bind<map_int64_t, 2>(m);
    bind<map_uint8_t, 2>(m);
    bind<map_uint16_t, 2>(m);
    bind<map_uint32_t, 2>(m);
    bind<map_uint64_t, 2>(m);
    bind<map_float_t, 2>(m);
    bind<map_double_t, 2>(m);
    bind<map_complexfloat_t, 2>(m);
    bind<map_complexdouble_t, 2>(m);
    // constmap
    bindconst<constmap_char_t, 2>(m);
    bindconst<constmap_int8_t, 2>(m);
    bindconst<constmap_int16_t, 2>(m);
    bindconst<constmap_int32_t, 2>(m);
    bindconst<constmap_int64_t, 2>(m);
    bindconst<constmap_uint8_t, 2>(m);
    bindconst<constmap_uint16_t, 2>(m);
    bindconst<constmap_uint32_t, 2>(m);
    bindconst<constmap_uint64_t, 2>(m);
    bindconst<constmap_float_t, 2>(m);
    bindconst<constmap_double_t, 2>(m);
    bindconst<constmap_complexfloat_t, 2>(m);
    bindconst<constmap_complexdouble_t, 2>(m);

    // 3d grids
    // heap
    bind<heap_char_t, 3>(m);
    bind<heap_int8_t, 3>(m);
    bind<heap_int16_t, 3>(m);
    bind<heap_int32_t, 3>(m);
    bind<heap_int64_t, 3>(m);
    bind<heap_uint8_t, 3>(m);
    bind<heap_uint16_t, 3>(m);
    bind<heap_uint32_t, 3>(m);
    bind<heap_uint64_t, 3>(m);
    bind<heap_float_t, 3>(m);
    bind<heap_double_t, 3>(m);
    bind<heap_complexfloat_t, 3>(m);
    bind<heap_complexdouble_t, 3>(m);
    // constheap
    bindconst<constheap_char_t, 3>(m);
    bindconst<constheap_int8_t, 3>(m);
    bindconst<constheap_int16_t, 3>(m);
    bindconst<constheap_int32_t, 3>(m);
    bindconst<constheap_int64_t, 3>(m);
    bindconst<constheap_uint8_t, 3>(m);
    bindconst<constheap_uint16_t, 3>(m);
    bindconst<constheap_uint32_t, 3>(m);
    bindconst<constheap_uint64_t, 3>(m);
    bindconst<constheap_float_t, 3>(m);
    bindconst<constheap_double_t, 3>(m);
    bindconst<constheap_complexfloat_t, 3>(m);
    bindconst<constheap_complexdouble_t, 3>(m);
    // map
    bind<map_char_t, 3>(m);
    bind<map_int8_t, 3>(m);
    bind<map_int16_t, 3>(m);
    bind<map_int32_t, 3>(m);
    bind<map_int64_t, 3>(m);
    bind<map_uint8_t, 3>(m);
    bind<map_uint16_t, 3>(m);
    bind<map_uint32_t, 3>(m);
    bind<map_uint64_t, 3>(m);
    bind<map_float_t, 3>(m);
    bind<map_double_t, 3>(m);
    bind<map_complexfloat_t, 3>(m);
    bind<map_complexdouble_t, 3>(m);
    // constmap
    bindconst<constmap_char_t, 3>(m);
    bindconst<constmap_int8_t, 3>(m);
    bindconst<constmap_int16_t, 3>(m);
    bindconst<constmap_int32_t, 3>(m);
    bindconst<constmap_int64_t, 3>(m);
    bindconst<constmap_uint8_t, 3>(m);
    bindconst<constmap_uint16_t, 3>(m);
    bindconst<constmap_uint32_t, 3>(m);
    bindconst<constmap_uint64_t, 3>(m);
    bindconst<constmap_float_t, 3>(m);
    bindconst<constmap_double_t, 3>(m);
    bindconst<constmap_complexfloat_t, 3>(m);
    bindconst<constmap_complexdouble_t, 3>(m);

    // 4d grids
    // heap
    bind<heap_char_t, 4>(m);
    bind<heap_int8_t, 4>(m);
    bind<heap_int16_t, 4>(m);
    bind<heap_int32_t, 4>(m);
    bind<heap_int64_t, 4>(m);
    bind<heap_uint8_t, 4>(m);
    bind<heap_uint16_t, 4>(m);
    bind<heap_uint32_t, 4>(m);
    bind<heap_uint64_t, 4>(m);
    bind<heap_float_t, 4>(m);
    bind<heap_double_t, 4>(m);
    bind<heap_complexfloat_t, 4>(m);
    bind<heap_complexdouble_t, 4>(m);
    // constheap
    bindconst<constheap_char_t, 4>(m);
    bindconst<constheap_int8_t, 4>(m);
    bindconst<constheap_int16_t, 4>(m);
    bindconst<constheap_int32_t, 4>(m);
    bindconst<constheap_int64_t, 4>(m);
    bindconst<constheap_uint8_t, 4>(m);
    bindconst<constheap_uint16_t, 4>(m);
    bindconst<constheap_uint32_t, 4>(m);
    bindconst<constheap_uint64_t, 4>(m);
    bindconst<constheap_float_t, 4>(m);
    bindconst<constheap_double_t, 4>(m);
    bindconst<constheap_complexfloat_t, 4>(m);
    bindconst<constheap_complexdouble_t, 4>(m);
    // map
    bind<map_char_t, 4>(m);
    bind<map_int8_t, 4>(m);
    bind<map_int16_t, 4>(m);
    bind<map_int32_t, 4>(m);
    bind<map_int64_t, 4>(m);
    bind<map_uint8_t, 4>(m);
    bind<map_uint16_t, 4>(m);
    bind<map_uint32_t, 4>(m);
    bind<map_uint64_t, 4>(m);
    bind<map_float_t, 4>(m);
    bind<map_double_t, 4>(m);
    bind<map_complexfloat_t, 4>(m);
    bind<map_complexdouble_t, 4>(m);
    // constmap
    bindconst<constmap_char_t, 4>(m);
    bindconst<constmap_int8_t, 4>(m);
    bindconst<constmap_int16_t, 4>(m);
    bindconst<constmap_int32_t, 4>(m);
    bindconst<constmap_int64_t, 4>(m);
    bindconst<constmap_uint8_t, 4>(m);
    bindconst<constmap_uint16_t, 4>(m);
    bindconst<constmap_uint32_t, 4>(m);
    bindconst<constmap_uint64_t, 4>(m);
    bindconst<constmap_float_t, 4>(m);
    bindconst<constmap_double_t, 4>(m);
    bindconst<constmap_complexfloat_t, 4>(m);
    bindconst<constmap_complexdouble_t, 4>(m);

    // all done
    return;
}


#if 0

#endif

// end of file
