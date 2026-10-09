// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// assemble the pipeline that paints the amplitude of a complex tile gray, the way an interactive
// editor would: nodes dropped from a palette, slots bound one at a time, settings changed, a stage
// swapped for another, and the whole thing let go; every observation an editor depends on is
// an assertion, so this walk through the c++ api stays true as the api changes


// portability
#include <portinfo>
// STL
#include <cassert>
#include <complex>
#include <memory>
#include <set>
#include <string>
#include <vector>
// support
#include <pyre/journal.h>
#include <pyre/viz.h>


// type aliases
// all tiles are two dimensional
using packing_t = pyre::grid::canonical_t<2>;
// the signal holds single precision complex cells, as a raster on disk might
using signal_grid_t = pyre::grid::grid_t<packing_t, pyre::memory::heap_t<std::complex<float>>>;
using signal_t = pyre::flow::products::tile_t<signal_grid_t>;
// the magnitudes are double precision
using real_grid_t = pyre::grid::grid_t<packing_t, pyre::memory::heap_t<double>>;
using real_t = pyre::flow::products::tile_t<real_grid_t>;
// the normalized values and the color channels are single precision
using channel_grid_t = pyre::grid::grid_t<packing_t, pyre::memory::heap_t<float>>;
using channel_t = pyre::flow::products::tile_t<channel_grid_t>;
// the encoded image
using image_t = pyre::viz::products::images::bmp_t;
// the factories
using selector_t = pyre::flow::factories::selectors::amplitude_t<signal_t, real_t>;
using normalizer_t = pyre::flow::factories::filters::parametric_t<real_t, channel_t>;
using colormap_t = pyre::viz::factories::colormaps::gray_t<channel_t>;
using codec_t = pyre::viz::factories::codecs::bmp_t<channel_t>;
// the protocols, which is all an editor sees once a node is on the canvas
using node_t = pyre::flow::protocols::Node;
using product_t = pyre::flow::protocols::Product;
using factory_t = pyre::flow::protocols::Factory;


// collect the nodes upstream of {product}, in the order a pull visits them: a product leads to
// the factories that write it, and a factory to the products bound to its inputs
auto
upstream(const std::shared_ptr<product_t> & product, std::vector<std::string> & names) -> void
{
    // record the product
    names.push_back(product->name());
    // go through the factories that write it
    for (const auto & [slot, writer] : product->writers()) {
        // the factory, which the product does not keep alive
        auto factory = writer.lock();
        // record it
        names.push_back(factory->name());
        // and go through its inputs
        for (const auto & [input, source] : factory->inputs()) {
            // each of which leads further upstream
            upstream(source.lock(), names);
        }
    }
    // all done
    return;
}


// driver
int
main(int argc, char * argv[])
{
    // the shape of the tiles
    auto shape = channel_t::shape_type(8, 8);
    // the record of what the nodes would be, once they are gone
    std::vector<std::weak_ptr<node_t>> nodes;

    // everything below lives in its own scope, so the end of it shows what is still alive
    {
        // 1. the palette: drop the nodes on the canvas, none of them connected yet
        // the products
        auto signal = signal_t::create("signal", shape, 0.0f);
        auto amplitude = real_t::create("amplitude", shape, 0.0);
        auto normalized = channel_t::create("normalized", shape, 0.0f);
        auto red = channel_t::create("red", shape, 0.0f);
        auto green = channel_t::create("green", shape, 0.0f);
        auto blue = channel_t::create("blue", shape, 0.0f);
        auto image = image_t::create("image", shape);
        // the factories
        auto selector = selector_t::create("amplitude");
        auto normalizer = normalizer_t::create("normalizer", { 0.0, 10.0 });
        auto colormap = colormap_t::create("gray");
        auto codec = codec_t::create("bmp");

        // a factory learns its slots only as they are bound: a fresh one has none, so the palette
        // cannot ask a factory what slots to draw, or what products they take
        assert(selector->inputs().empty() && selector->outputs().empty());
        // tiles start out clean, as if they held something worth reading
        assert(!signal->stale() && !amplitude->stale() && !red->stale());
        // while the image starts out stale
        assert(image->stale());

        // 2. the wiring: bind each slot, with the setters that know the type of the product
        // the selector reads the signal and writes the magnitudes
        selector->signal(signal);
        selector->amplitude(amplitude);
        // the normalizer reads the magnitudes and writes the normalized values
        normalizer->signal(amplitude);
        normalizer->normalized(normalized);
        // the colormap reads the normalized values and paints the three channels
        colormap->data(normalized);
        colormap->red(red);
        colormap->green(green);
        colormap->blue(blue);
        // the codec reads the three channels and encodes the image
        codec->red(red);
        codec->green(green);
        codec->blue(blue);
        codec->image(image);

        // every binding is visible from both of its ends: the signal knows who reads it
        assert(signal->readers().size() == 1);
        // and the selector knows what it reads, by slot
        assert(selector->input("signal") == signal);
        // a product written by a factory knows its writer
        assert(amplitude->writers().size() == 1);
        // binding an output flushes the product, so everything a factory writes is now stale
        assert(amplitude->stale() && normalized->stale() && red->stale() && image->stale());
        // while binding an input does not, so the signal, which nobody writes, is still clean
        assert(!signal->stale());

        // 3. walking the graph: everything a canvas draws is reachable from the image
        std::vector<std::string> names;
        upstream(image, names);
        // in the order a pull visits it
        auto expected = std::vector<std::string> {
            "image",      "bmp",        "blue",      "gray",      "normalized", "normalizer",
            "amplitude",  "amplitude",  "signal",    "green",     "gray",       "normalized",
            "normalizer", "amplitude",  "amplitude", "signal",    "red",        "gray",
            "normalized", "normalizer", "amplitude", "amplitude", "signal"
        };
        // the codec reads three channels, so the walk passes the shared part of the graph three
        // times; a canvas has to fold a walk into a set of nodes
        assert(names == expected);
        // the distinct nodes
        auto distinct = std::set<std::string>(names.begin(), names.end());
        // name the eleven nodes on the canvas, with the selector and its output sharing a name
        assert(distinct.size() == 10);

        // 4. the first pull: fill the signal with magnitudes 0 through 63
        auto & cells = signal->write();
        // one per cell
        for (int cell = 0; cell < 64; ++cell) {
            // at a phase that varies with the cell, so the magnitude is not just the real part
            cells[cell] = std::polar(static_cast<float>(cell), 0.1f * cell);
        }
        // the wiring left every stage stale, so a pull of the image runs all of them
        image->read();
        // the magnitudes are there
        assert(std::abs(amplitude->read()[5] - 5.0) < 1e-5);
        // and so are the colors: a magnitude of 5 in [0, 10] is half way to white
        assert(std::abs(red->read()[5] - 0.5) < 1e-5);
        // and everything is fresh
        assert(!amplitude->stale() && !red->stale() && !image->stale());

        // a new tile in the same signal: twice the magnitudes
        for (int cell = 0; cell < 64; ++cell) {
            // at the same phases
            cells[cell] = std::polar(2.0f * cell, 0.1f * cell);
        }
        // writing into a tile does not tell anybody, so a pull finds everything fresh
        image->read();
        // and the image still shows the old tile
        assert(std::abs(red->read()[5] - 0.5) < 1e-5);
        // the signal has to be flushed after it is filled, which makes everything downstream stale
        signal->flush();
        // all the way to the image
        assert(amplitude->stale() && normalized->stale() && red->stale() && image->stale());
        // and now a pull runs every stage
        image->read();
        // a magnitude of 10 in [0, 10] is white
        assert(std::abs(red->read()[5] - 1.0) < 1e-5);
        // put the first tile back, for the steps below
        for (int cell = 0; cell < 64; ++cell) {
            // the magnitudes 0 through 63
            cells[cell] = std::polar(static_cast<float>(cell), 0.1f * cell);
        }
        // say so
        signal->flush();
        // and repaint
        image->read();
        // back to half way to white
        assert(std::abs(red->read()[5] - 0.5) < 1e-5);

        // 5. a setting: a new interval for the normalizer
        normalizer->interval({ 0.0, 20.0 });
        // makes stale everything downstream of the normalizer
        assert(normalized->stale() && red->stale() && image->stale());
        // and nothing upstream of it, so the magnitudes are not computed again
        assert(!amplitude->stale());
        // the pull repaints with the new interval
        image->read();
        // a magnitude of 5 in [0, 20] is a quarter of the way to white
        assert(std::abs(red->read()[5] - 0.25) < 1e-5);

        // 6. a swap: replace the normalizer with one that has a different interval
        auto replacement = normalizer_t::create("replacement", { 0.0, 40.0 });
        // unbind the old one from both of its products
        normalizer->removeInput("signal");
        normalizer->removeOutput("normalized");
        // and bind the new one in its place
        replacement->signal(amplitude);
        replacement->normalized(normalized);
        // binding its output flushed the normalized values, and everything downstream of them
        assert(normalized->stale() && image->stale());
        // so the next pull repaints
        image->read();
        // a magnitude of 5 in [0, 40] is an eighth of the way to white
        assert(std::abs(red->read()[5] - 0.125) < 1e-5);

        // a rebinding of an input alone is another matter: a second signal, with twice the
        // magnitudes
        auto other = signal_t::create("other", shape, 0.0f);
        // filled
        auto & doubled = other->write();
        // cell by cell
        for (int cell = 0; cell < 64; ++cell) {
            // at the same phases
            doubled[cell] = std::polar(2.0f * cell, 0.1f * cell);
        }
        // takes the place of the first one at the input of the selector
        selector->removeInput("signal");
        selector->signal(other);
        // which flushed nothing: the magnitudes still describe the first signal
        assert(!amplitude->stale() && !image->stale());
        // the editor has to flush the factory it rebound, which makes its outputs stale
        selector->flush();
        // so the next pull repaints
        image->read();
        // a magnitude of 10 in [0, 40] is a quarter of the way to white
        assert(std::abs(red->read()[5] - 0.25) < 1e-5);

        // 7. types: the generic binding takes any product, whatever its type
        auto stray = selector_t::create("stray");
        // so a tile of magnitudes is accepted where the signal belongs
        stray->addInput("signal", amplitude);
        // the binding is recorded
        assert(stray->input("signal") == amplitude);
        // but the typed accessor cannot see it, and a pull through this factory would read from
        // nothing; only the typed setters check the type, and they do it at compile time
        assert(stray->signal() == nullptr);
        // undo the binding
        stray->removeInput("signal");

        // 8. the record of the nodes, before the scope that holds them closes
        nodes = { signal, other,    amplitude,  normalized,  red,      green, blue,
                  image,  selector, normalizer, replacement, colormap, codec };
        // factories own their outputs and refer to everything else weakly, so nothing holds
        // the graph together but the references in this scope, which go away with it
    }

    // so nothing outlives the scope, although no binding was undone
    for (const auto & node : nodes) {
        // every one of them is gone
        assert(node.expired());
    }

    // all done
    return 0;
}


// end of file
