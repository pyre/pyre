// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// file creation property lists
void
pyre::h5::py::properties::fcpl(py::module & m)
{
    // add bindings for hdf5 file creation property lists
    auto cls = py::class_<FCPL, PropList>(
        // in scope
        m,
        // class name
        "fcpl",
        // docstring
        "a file creation property list");

    // static properties
    cls.def_property_readonly_static(
        // the name
        "default",
        // the implementation
        [](const py::object &) -> const FCPL & {
            // easy enough
            return FCPL::theDefault();
        },
        // we hand back a reference to a shared, library-owned object
        py::return_value_policy::reference,
        // docstring
        "the default file creation property list");

    // constructor
    cls.def(
        // the implementation
        py::init(),
        // the docstring
        "build a file creation property list");

    // interface
    // the file space page size
    cls.def_property(
        // the name
        "pageSize",
        // the getter
        &FCPL::pageSize,
        // the setter
        &FCPL::setPageSize,
        // the docstring
        "the size of the pages my file space is carved into");

    // the file space strategy
    cls.def_property(
        // the name
        "filespaceStrategy",
        // the getter
        &FCPL::filespaceStrategy,
        // the setter, which unpacks the {(strategy, persist, threshold)} triplet
        [](FCPL & self,
           const std::tuple<H5F_fspace_strategy_t, bool, hsize_t> & strategy) -> void {
            // spread the triplet
            auto [approach, persist, threshold] = strategy;
            // and hand it to the property list
            self.setFilespaceStrategy(approach, persist, threshold);
            // all done
            return;
        },
        // the docstring
        "how free space is managed, as {(strategy, persist, threshold)}");

    // the user block
    cls.def_property(
        // the name
        "userblock",
        // the getter
        &FCPL::userblock,
        // the setter
        &FCPL::setUserblock,
        // the docstring
        "the size of the byte range at the front of my file that hdf5 leaves alone");

    // the widths used to record positions and lengths
    cls.def_property(
        // the name
        "sizes",
        // the getter
        &FCPL::sizes,
        // the setter, which unpacks the {(offset bytes, length bytes)} pair
        [](FCPL & self, const std::tuple<std::size_t, std::size_t> & sizes) -> void {
            // spread the pair
            auto [offsets, lengths] = sizes;
            // and hand it to the property list
            self.setSizes(offsets, lengths);
            // all done
            return;
        },
        // the docstring
        "the widths used to record positions and lengths, as {(offset, length)} bytes");

    // all done
    return;
}


// end of file
