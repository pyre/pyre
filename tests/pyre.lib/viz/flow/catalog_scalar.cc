// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// check that a catalog makes scalars, which have no shape, by the spelling of their type, and
// that their entries name no cells, so they are never mistaken for tiles


// portability
#include <portinfo>
// STL
#include <cassert>
// support
#include <pyre/viz.h>


// type aliases
// the shape of a graph
using shape_t = pyre::grid::canonical_t<2>::shape_type;
// the scalars
using scalar_t = pyre::flow::products::var_t<double>;
// the catalog
using catalog_t = pyre::flow::catalog::catalog_t;


// driver
int
main(int argc, char * argv[])
{
    // make a catalog
    auto catalog = catalog_t();
    // register the scalars
    const auto & entry = catalog.registerProduct<scalar_t>();

    // the entry is filed under the spelling of their type
    assert(catalog.product(scalar_t::declSelf()) == &entry);
    // with their readable name
    assert(entry.className() == "VariableDouble");
    // the catalog can make them
    assert(entry.makes());
    // and they are no grids of cells, so they name no cells
    assert(entry.cell().empty());

    // make one by the spelling of its type, with a name and the shape of the graph
    auto product = catalog.makeProduct(scalar_t::declSelf(), "scale", shape_t { 3, 5 });
    // which is a scalar
    auto scalar = std::dynamic_pointer_cast<scalar_t>(product);
    assert(scalar);
    // with the name
    assert(scalar->name() == "scale");
    // and the zero of its type, since nobody has written it yet
    assert(scalar->read() == 0);

    // all done
    return 0;
}


// end of file
