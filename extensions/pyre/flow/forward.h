// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// the {flow} bindings
namespace pyre::py::flow {
    // the catalog of the kinds of nodes this extension was compiled with, which every subpackage
    // that binds nodes registers its kinds with
    auto registry() -> catalog_t &;

    // register the classes of the protocols of nodes, products, and factories
    void nodeClasses(py::module &);
    // of the descriptions of the slots and the settings of factories
    void descriptionClasses(py::module &);
    // of the catalog and its entries
    void catalogClasses(py::module &);
    // and of the tiles, the variables, and the rasters over python buffers
    void tileClasses(py::module &);
    void variableClasses(py::module &);
    void rasterClasses(py::module &);

    // the protocols of nodes, products, and factories
    void nodes();
    // the descriptions of the slots and the settings of factories
    void descriptions();
    // the catalog and its entries
    void catalog(py::module &);
    // the tiles, the variables, the rasters over python buffers, and the factories of
    // {pyre::flow}, which go in the catalog as well
    void tiles();
    void variables();
    void rasters(py::module &);
    void factories(py::module &);
} // namespace pyre::py::flow


// end of file
