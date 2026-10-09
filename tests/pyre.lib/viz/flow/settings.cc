// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// check that a factory describes its settings, and that they can be read and changed by name,
// without knowing the concrete type of the factory, the way an inspector does


// portability
#include <portinfo>
// STL
#include <cassert>
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
using float64_t = tile_t<double>;
using float32_t = tile_t<float>;
// the factories
using normalizer_t = pyre::flow::factories::filters::parametric_t<float64_t, float32_t>;
using colormap_t = pyre::viz::factories::colormaps::gray_t<float32_t>;
// intervals
using interval_t = pyre::flow::interval_t;


// driver
int
main(int argc, char * argv[])
{
    // make a normalizer
    auto normalizer = normalizer_t::create("normalizer", { 0, 10 });
    // reach it through the protocol
    std::shared_ptr<pyre::flow::factory_t> factory = normalizer;

    // it describes one setting
    const auto & settings = factory->settings();
    assert(settings.size() == 1);
    // its interval
    assert(settings[0].name() == "interval");
    assert(settings[0].type() == "interval");
    // which reads as the one it was made with
    assert(std::get<interval_t>(*factory->get("interval")) == interval_t(0, 10));
    // while a setting it does not have has no value
    assert(!factory->get("level"));

    // wire it up and pull the output, so it is fresh
    auto shape = shape_t { 2, 2 };
    auto signal = float64_t::create("signal", shape, 5.0);
    auto normalized = float32_t::create("normalized", shape, 0.0f);
    factory->bind("signal", signal);
    factory->bind("normalized", normalized);
    normalized->read();
    assert(!normalized->stale());

    // a new interval, by name
    assert(factory->set("interval", interval_t { 0, 20 }));
    // is in place
    assert(normalizer->interval() == interval_t(0, 20));
    // and makes the output stale
    assert(normalized->stale());
    // a value of the wrong type is refused
    assert(!factory->set("interval", 3.0));
    // and leaves the interval as it was
    assert(normalizer->interval() == interval_t(0, 20));
    // and so is a setting it does not have
    assert(!factory->set("level", 3));

    // a colormap with no settings describes none
    assert(colormap_t::create("gray")->settings().empty());

    // take the graph apart
    factory->unbind("signal");
    factory->unbind("normalized");

    // all done
    return 0;
}


// end of file
