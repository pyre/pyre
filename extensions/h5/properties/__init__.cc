// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// the package global declarations
#include "../__init__.h"
// the local declarations
#include "__init__.h"
// namespace setup
#include "forward.h"


// make the namespace of the property lists, and register their classes in it, so that every
// signature can name them
void
pyre::h5::py::properties::classes(py::module & m)
{
    // make a new namespace to hold the property list classes
    auto properties = m.def_submodule(
        // the name of the module
        "properties",
        // its docstring
        "HDF5 property lists");

    // the values the lists trade in
    chunkCacheClass(properties);
    alignmentClass(properties);
    cacheClass(properties);
    pageBufferClass(properties);
    versionBoundsClass(properties);
    filespaceStrategyClass(properties);
    sizesClass(properties);
    phaseChangeClass(properties);
    linkEstimateClass(properties);
    filterClass(properties);
    // the generic base
    plClass(properties);
    // the properties shared by everything one creates, before the concrete creation lists that
    // derive from it
    ocplClass(properties);
    // and by everything that lays down a name
    strcplClass(properties);
    // dataset access, creation, and transfer
    daplClass(properties);
    dcplClass(properties);
    dxplClass(properties);
    // file access and creation
    faplClass(properties);
    fcplClass(properties);
    // group creation
    gcplClass(properties);
    // link access and creation
    laplClass(properties);
    lcplClass(properties);
    // attribute creation
    acplClass(properties);

    // all done
    return;
}


// property lists
void
pyre::h5::py::properties::__init__()
{
    // the values the lists trade in
    chunkCache();
    alignment();
    cache();
    pageBuffer();
    versionBounds();
    filespaceStrategy();
    sizes();
    phaseChange();
    linkEstimate();
    filter();
    // the generic base
    pl();
    // the properties shared by everything one creates
    ocpl();
    // and by everything that lays down a name
    strcpl();
    // dataset access, creation, and transfer
    dapl();
    dcpl();
    dxpl();
    // file access and creation
    fapl();
    fcpl();
    // group creation
    gcpl();
    // link access and creation
    lapl();
    lcpl();
    // attribute creation
    acpl();

    // all done
    return;
}


// end of file
