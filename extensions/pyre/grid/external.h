// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_py_grid_external_h)
#define pyre_py_grid_external_h


// get the common ones
#include "../external.h"
// get the pyre parts
#include <pyre/grid.h>

namespace pyre::py::grid {
    // aliases
    // heap
    using heap_char_t = pyre::memory::heap_t<char>;
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

    // constheap
    using constheap_char_t = pyre::memory::constheap_t<char>;
    using constheap_int8_t = pyre::memory::constheap_t<std::int8_t>;
    using constheap_int16_t = pyre::memory::constheap_t<std::int16_t>;
    using constheap_int32_t = pyre::memory::constheap_t<std::int32_t>;
    using constheap_int64_t = pyre::memory::constheap_t<std::int64_t>;
    using constheap_uint8_t = pyre::memory::constheap_t<std::uint8_t>;
    using constheap_uint16_t = pyre::memory::constheap_t<std::uint16_t>;
    using constheap_uint32_t = pyre::memory::constheap_t<std::uint32_t>;
    using constheap_uint64_t = pyre::memory::constheap_t<std::uint64_t>;
    using constheap_float_t = pyre::memory::constheap_t<float>;
    using constheap_double_t = pyre::memory::constheap_t<double>;
    using constheap_complexfloat_t = pyre::memory::constheap_t<std::complex<float>>;
    using constheap_complexdouble_t = pyre::memory::constheap_t<std::complex<double>>;

    // map
    using map_char_t = pyre::memory::map_t<char>;
    using map_int8_t = pyre::memory::map_t<std::int8_t>;
    using map_int16_t = pyre::memory::map_t<std::int16_t>;
    using map_int32_t = pyre::memory::map_t<std::int32_t>;
    using map_int64_t = pyre::memory::map_t<std::int64_t>;
    using map_uint8_t = pyre::memory::map_t<std::uint8_t>;
    using map_uint16_t = pyre::memory::map_t<std::uint16_t>;
    using map_uint32_t = pyre::memory::map_t<std::uint32_t>;
    using map_uint64_t = pyre::memory::map_t<std::uint64_t>;
    using map_float_t = pyre::memory::map_t<float>;
    using map_double_t = pyre::memory::map_t<double>;
    using map_complexfloat_t = pyre::memory::map_t<std::complex<float>>;
    using map_complexdouble_t = pyre::memory::map_t<std::complex<double>>;

    // constmap
    using constmap_char_t = pyre::memory::constmap_t<char>;
    using constmap_int8_t = pyre::memory::constmap_t<std::int8_t>;
    using constmap_int16_t = pyre::memory::constmap_t<std::int16_t>;
    using constmap_int32_t = pyre::memory::constmap_t<std::int32_t>;
    using constmap_int64_t = pyre::memory::constmap_t<std::int64_t>;
    using constmap_uint8_t = pyre::memory::constmap_t<std::uint8_t>;
    using constmap_uint16_t = pyre::memory::constmap_t<std::uint16_t>;
    using constmap_uint32_t = pyre::memory::constmap_t<std::uint32_t>;
    using constmap_uint64_t = pyre::memory::constmap_t<std::uint64_t>;
    using constmap_float_t = pyre::memory::constmap_t<float>;
    using constmap_double_t = pyre::memory::constmap_t<double>;
    using constmap_complexfloat_t = pyre::memory::constmap_t<std::complex<float>>;
    using constmap_complexdouble_t = pyre::memory::constmap_t<std::complex<double>>;


} // namespace pyre::py::grid


#endif

// end of file
