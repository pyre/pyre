// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// check that ownership follows the data: a factory owns its outputs and refers to its inputs
// weakly, and a product refers to its readers and writers weakly, so a graph goes away when its
// client lets go of it, and dropping a factory never keeps what is upstream of it alive


// portability
#include <portinfo>
// STL
#include <cassert>
#include <memory>
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
    auto shape = shape_t { 2, 2 };

    // a factory keeps its output alive, but not its input
    {
        // make a factory
        auto normalizer = normalizer_t::create("normalizer", { 0, 10 });
        // and its products, remembering them weakly
        std::weak_ptr<float64_t> signal;
        std::weak_ptr<float32_t> normalized;
        {
            // the products, held only in this scope
            auto input = float64_t::create("signal", shape, 5.0);
            auto output = float32_t::create("normalized", shape, 0.0f);
            // bound to the factory
            normalizer->signal(input);
            normalizer->normalized(output);
            // remembered
            signal = input;
            normalized = output;
        }
        // the input is gone, since nothing but the factory referred to it
        assert(signal.expired());
        // and the factory sees that it is gone
        assert(normalizer->input("signal") == nullptr);
        // while the output is alive, since the factory owns it
        assert(!normalized.expired());
        // and undoing a binding whose product is gone is harmless
        normalizer->removeInput("signal");
        assert(normalizer->inputs().empty());
    }

    // a product does not keep its writer alive
    {
        // the input, held here
        auto input = float64_t::create("signal", shape, 5.0);
        // the output, held here as well
        auto output = float32_t::create("normalized", shape, 0.0f);
        // and the factory, remembered weakly
        std::weak_ptr<normalizer_t> factory;
        {
            // make a factory, held only in this scope
            auto normalizer = normalizer_t::create("normalizer", { 0, 10 });
            // bind it
            normalizer->signal(input);
            normalizer->normalized(output);
            // pull the output, which is half way through the interval
            assert(output->read()[0] == 0.5f);
            // remember the factory
            factory = normalizer;
        }
        // the factory is gone, since nothing but its products referred to it
        assert(factory.expired());
        // so a change upstream
        input->write()[0] = 10.0;
        input->flush();
        // leaves the output fresh, since the factory that linked them is gone
        assert(!output->stale());
        // the output keeps what it had, since nothing can remake it
        assert(output->read()[0] == 0.5f);
    }

    // all done
    return 0;
}


// end of file
