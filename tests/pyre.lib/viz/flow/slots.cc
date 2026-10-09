// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// check that a factory describes its slots before anything is bound, and that binding a slot by
// name is checked against them: a slot it does not have, or a product of the wrong type, binds
// nothing; binding an input makes the factory's outputs stale; binding again replaces


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
// the factory
using normalizer_t = pyre::flow::factories::filters::parametric_t<float64_t, float32_t>;


// driver
int
main(int argc, char * argv[])
{
    // the shape of the tiles
    auto shape = shape_t { 4, 4 };
    // make a factory
    auto normalizer = normalizer_t::create("normalizer");
    // reach it through the protocol, the way an editor does
    std::shared_ptr<pyre::flow::factory_t> factory = normalizer;

    // it describes its slots before anything is bound
    const auto & slots = factory->slots();
    // two of them
    assert(slots.size() == 2);
    // an input that takes tiles of doubles
    assert(slots[0].name() == "signal");
    assert(slots[0].reads() && !slots[0].writes());
    assert(slots[0].product() == float64_t::declSelf());
    // and an output that takes tiles of floats
    assert(slots[1].name() == "normalized");
    assert(slots[1].writes() && !slots[1].reads());
    assert(slots[1].product() == float32_t::declSelf());
    // which it can find by name
    assert(factory->slot("normalized") == &slots[1]);
    // but not one it does not have
    assert(factory->slot("data") == nullptr);

    // the products
    auto signal = float64_t::create("signal", shape, 0.0);
    auto normalized = float32_t::create("normalized", shape, 0.0f);
    // a tile of the wrong type
    auto wrong = float32_t::create("wrong", shape, 0.0f);

    // a slot it does not have binds nothing
    assert(!factory->bind("data", signal));
    // nor does a product of the wrong type
    assert(!factory->bind("signal", wrong));
    // so nothing is bound
    assert(factory->inputs().empty() && factory->outputs().empty());

    // the right products bind
    assert(factory->bind("signal", signal));
    assert(factory->bind("normalized", normalized));
    // and are where they belong
    assert(factory->input("signal") == signal);
    assert(factory->output("normalized") == normalized);
    // so the typed accessors see them
    assert(normalizer->signal() == signal);

    // pull the output, so it is fresh
    normalized->read();
    assert(!normalized->stale());
    // binding the input again
    auto other = float64_t::create("other", shape, 1.0);
    assert(factory->bind("signal", other));
    // replaces the old binding
    assert(factory->input("signal") == other);
    assert(factory->inputs().size() == 1);
    // and makes the output stale, since it depends on the input
    assert(normalized->stale());

    // undoing the bindings
    assert(factory->unbind("signal"));
    assert(factory->unbind("normalized"));
    // leaves nothing bound
    assert(factory->inputs().empty() && factory->outputs().empty());
    // and undoing them again does nothing
    assert(!factory->unbind("signal"));
    // nor does undoing one of a slot it does not have
    assert(!factory->unbind("data"));

    // all done
    return 0;
}


// end of file
