// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// what the page buffer of a file has seen
void
pyre::h5::py::pageBufferStats(py::module & m)
{
    // add bindings for the record
    auto cls = py::class_<PageBufferStats>(
        // in scope
        m,
        // class name
        "PageBufferStats",
        // docstring
        "what the page buffer of a file has seen; every count is a pair, metadata first and "
        "raw data second");

    // the requests the buffer was asked to serve
    cls.def_readonly(
        // the name
        "accesses",
        // the field
        &PageBufferStats::accesses,
        // the docstring
        "the requests the buffer was asked to serve, as {(metadata, raw)}");

    // the ones it served from a page it already held
    cls.def_readonly(
        // the name
        "hits",
        // the field
        &PageBufferStats::hits,
        // the docstring
        "the requests served from a page the buffer already held, as {(metadata, raw)}");

    // the ones that sent it to the file
    cls.def_readonly(
        // the name
        "misses",
        // the field
        &PageBufferStats::misses,
        // the docstring
        "the requests that sent the buffer to the file for a page, as {(metadata, raw)}");

    // the pages it let go of
    cls.def_readonly(
        // the name
        "evictions",
        // the field
        &PageBufferStats::evictions,
        // the docstring
        "the pages the buffer let go of to make room, as {(metadata, raw)}");

    // the requests that went around it
    cls.def_readonly(
        // the name
        "bypasses",
        // the field
        &PageBufferStats::bypasses,
        // the docstring
        "the requests too large for a page, which went to the file without the buffer, as "
        "{(metadata, raw)}");

    // all done
    return;
}


// end of file
