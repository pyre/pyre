// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// check that a catalog files the kinds of nodes registered with it under the spellings of their
// types, describes them before any node of their kind exists, and makes nodes by name


// portability
#include <portinfo>
// STL
#include <cassert>
#include <complex>
// support
#include <pyre/viz.h>


// type aliases
// all tiles are two dimensional
using packing_t = pyre::grid::canonical_t<2>;
using shape_t = packing_t::shape_type;
// a tile over cells of a given type
template <typename cellT>
using tile_t =
    pyre::flow::products::tile_t<pyre::grid::grid_t<packing_t, pyre::memory::heap_t<cellT>>>;
// the tiles
using complex64_t = tile_t<std::complex<float>>;
using float64_t = tile_t<double>;
using float32_t = tile_t<float>;
// the encoded image
using image_t = pyre::viz::products::images::bmp_t;
// the factories
using amplitude_t = pyre::flow::factories::selectors::amplitude_t<complex64_t, float64_t>;
using normalizer_t = pyre::flow::factories::filters::parametric_t<float64_t, float32_t>;
// the catalog
using catalog_t = pyre::flow::catalog::catalog_t;


// driver
int
main(int argc, char * argv[])
{
    // make a catalog
    auto catalog = catalog_t();
    // register the tiles
    catalog.registerProduct<complex64_t>();
    catalog.registerProduct<float64_t>();
    catalog.registerProduct<float32_t>();
    // the image
    catalog.registerProduct<image_t>();
    // and two factories
    catalog.registerFactory<amplitude_t>();
    const auto & entry = catalog.registerFactory<normalizer_t>();

    // it knows four kinds of products and two of factories
    assert(catalog.products().size() == 4);
    assert(catalog.factories().size() == 2);
    // registering a kind again replaces its entry
    catalog.registerProduct<float32_t>();
    assert(catalog.products().size() == 4);

    // the entry of the normalizer is filed under the spelling of its type
    assert(catalog.factory(normalizer_t::declSelf()) == &entry);
    // with its readable name
    assert(entry.className() == "Parametric");
    // its slots, before any normalizer exists
    assert(entry.slots().size() == 2);
    assert(entry.slots()[0].name() == "signal");
    // naming the products they take, which the catalog also knows
    assert(catalog.product(entry.slots()[0].product()) != nullptr);
    // and its settings
    assert(entry.settings().size() == 1);
    assert(entry.settings()[0].name() == "interval");
    // a tile's entry spells the type of its cells
    assert(catalog.product(float64_t::declSelf())->cell() == "double");
    // while the image, which is no grid of cells, has none
    assert(catalog.product(image_t::declSelf())->cell().empty());
    // while a type it does not know has no entry
    assert(catalog.factory("pyre::flow::factories::filters::nothing_t") == nullptr);

    // make a tile by the spelling of its type, with a name and a shape
    auto product = catalog.makeProduct(float64_t::declSelf(), "magnitude", shape_t { 3, 5 });
    // which is a tile of doubles
    auto tile = std::dynamic_pointer_cast<float64_t>(product);
    assert(tile);
    // with the name
    assert(tile->name() == "magnitude");
    // and the shape it was asked for
    assert(tile->shape() == shape_t(3, 5));
    // with every cell set to zero
    for (auto cell : tile->read()) {
        // one at a time
        assert(cell == 0);
    }
    // make an image the same way
    auto image = std::dynamic_pointer_cast<image_t>(
        catalog.makeProduct(image_t::declSelf(), "image", shape_t { 3, 5 }));
    // which has the shape it was asked for
    assert(image && image->shape() == shape_t(3, 5));

    // make a factory by the spelling of its type
    auto factory = catalog.makeFactory(normalizer_t::declSelf(), "normalizer");
    // which is a normalizer
    assert(std::dynamic_pointer_cast<normalizer_t>(factory));
    // with the name
    assert(factory->name() == "normalizer");
    // which binds the tile the catalog made
    assert(factory->bind("signal", tile));
    // and undoes it
    assert(factory->unbind("signal"));

    // a type the catalog does not know makes nothing
    assert(catalog.makeFactory("pyre::flow::factories::filters::nothing_t", "nothing") == nullptr);
    assert(catalog.makeProduct("nothing", "nothing", shape_t { 1, 1 }) == nullptr);

    // all done
    return 0;
}


// end of file
