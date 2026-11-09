// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// externals
#include "../external.h"


// the local binders
namespace pyre::h5::py::properties {
    // register the classes of the values a property list trades in
    void chunkCacheClass(py::module &);
    void alignmentClass(py::module &);
    void cacheClass(py::module &);
    void pageBufferClass(py::module &);
    void versionBoundsClass(py::module &);
    void filespaceStrategyClass(py::module &);
    void sizesClass(py::module &);
    void phaseChangeClass(py::module &);
    void linkEstimateClass(py::module &);
    void filterClass(py::module &);
    // the generic base
    void plClass(py::module &);
    // the properties shared by everything one creates
    void ocplClass(py::module &);
    // the properties shared by everything that lays down a name
    void strcplClass(py::module &);
    // dataset access, creation, and transfer
    void daplClass(py::module &);
    void dcplClass(py::module &);
    void dxplClass(py::module &);
    // file access and creation
    void faplClass(py::module &);
    void fcplClass(py::module &);
    // group creation
    void gcplClass(py::module &);
    // link access and creation
    void laplClass(py::module &);
    void lcplClass(py::module &);
    // attribute creation
    void acplClass(py::module &);

    // bind the values a property list trades in
    void chunkCache();
    void alignment();
    void cache();
    void pageBuffer();
    void versionBounds();
    void filespaceStrategy();
    void sizes();
    void phaseChange();
    void linkEstimate();
    void filter();
    // the generic base
    void pl();
    // the properties shared by everything one creates
    void ocpl();
    // the properties shared by everything that lays down a name
    void strcpl();
    // dataset access, creation, and transfer
    void dapl();
    void dcpl();
    void dxpl();
    // file access and creation
    void fapl();
    void fcpl();
    // group creation
    void gcpl();
    // link access and creation
    void lapl();
    void lcpl();
    // attribute creation
    void acpl();
} // namespace pyre::h5::py::properties


// end of file
