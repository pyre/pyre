// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"

// my package declarations
#include "__init__.h"
// my subpackages
#include "properties/__init__.h"
#include "types/__init__.h"

// the module entry point
PYBIND11_MODULE(h5, m)
{
    // the docstring
    m.doc() = "the hdf5 extension module";

    // register the module api
    pyre::h5::py::api(m);
    // enums
    pyre::h5::py::enums(m);

    // register every class before binding any interface, since the signatures name the
    // classes they traffic in, across the subpackages: the property lists and the datatypes
    pyre::h5::py::properties::classes(m);
    pyre::h5::py::types::classes(m);
    // the objects, the group before the file that derives from it
    pyre::h5::py::dataspaceClass(m);
    pyre::h5::py::attributeClass(m);
    pyre::h5::py::chunkClass(m);
    pyre::h5::py::datasetClass(m);
    pyre::h5::py::groupClass(m);
    pyre::h5::py::pageBufferStatsClass(m);
    pyre::h5::py::fileClass(m);
    // and the module-local flavors of the type-erased grid and mosaic
    pyre::h5::py::mosaicClasses(m);

    // now bind their interfaces: the subpackages
    pyre::h5::py::properties::__init__();
    pyre::h5::py::types::__init__(m);
    // the objects
    pyre::h5::py::dataspace(m);
    pyre::h5::py::attribute();
    pyre::h5::py::chunk();
    pyre::h5::py::dataset();
    pyre::h5::py::group();
    pyre::h5::py::pageBufferStats();
    pyre::h5::py::file();
    // the module-local flavors of the type-erased grid and mosaic
    pyre::h5::py::mosaics();

    // all done
    return;
}


// end of file
