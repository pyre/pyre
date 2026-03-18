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


namespace pyre::py::grid {
void
grids_4d(py::module & m)
{
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
    // view
    bind<view_char_t, 4>(m);
    bind<view_int8_t, 4>(m);
    bind<view_int16_t, 4>(m);
    bind<view_int32_t, 4>(m);
    bind<view_int64_t, 4>(m);
    bind<view_uint8_t, 4>(m);
    bind<view_uint16_t, 4>(m);
    bind<view_uint32_t, 4>(m);
    bind<view_uint64_t, 4>(m);
    bind<view_float_t, 4>(m);
    bind<view_double_t, 4>(m);
    bind<view_complexfloat_t, 4>(m);
    bind<view_complexdouble_t, 4>(m);
    // constview
    bindconst<constview_char_t, 4>(m);
    bindconst<constview_int8_t, 4>(m);
    bindconst<constview_int16_t, 4>(m);
    bindconst<constview_int32_t, 4>(m);
    bindconst<constview_int64_t, 4>(m);
    bindconst<constview_uint8_t, 4>(m);
    bindconst<constview_uint16_t, 4>(m);
    bindconst<constview_uint32_t, 4>(m);
    bindconst<constview_uint64_t, 4>(m);
    bindconst<constview_float_t, 4>(m);
    bindconst<constview_double_t, 4>(m);
    bindconst<constview_complexfloat_t, 4>(m);
    bindconst<constview_complexdouble_t, 4>(m);

    // all done
    return;
}
} // namespace pyre::py::grid


// end of file
