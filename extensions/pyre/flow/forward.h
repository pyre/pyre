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

    // the protocols of nodes, products, and factories
    void nodes(py::module &);
    // the descriptions of the slots and the settings of factories
    void descriptions(py::module &);
    // the catalog and its entries
    void catalog(py::module &);
    // the tiles, and the factories of {pyre::flow}, which go in the catalog as well
    void tiles(py::module &);
    void factories(py::module &);
} // namespace pyre::py::flow


// end of file
