// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// check the rule that makes it safe for a flush to stop at a product that is stale already: a
// stale product has nothing fresh downstream of it; every way of binding, writing, setting, and
// pulling keeps the rule, a cycle flushes in finite time, and a factory that cannot read one of
// its inputs says so instead of computing


// portability
#include <portinfo>
// STL
#include <cassert>
#include <cmath>
#include <complex>
#include <memory>
#include <vector>
// support
#include <pyre/journal.h>
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
// the image
using image_t = pyre::viz::products::images::bmp_t;
// the factories
using selector_t = pyre::flow::factories::selectors::amplitude_t<complex64_t, float64_t>;
using normalizer_t = pyre::flow::factories::filters::parametric_t<float64_t, float32_t>;
using colormap_t = pyre::viz::factories::colormaps::gray_t<float32_t>;
using codec_t = pyre::viz::factories::codecs::bmp_t<float32_t>;
// the loop: a filter that reads and writes tiles of the same type
using loop_t = pyre::flow::factories::filters::parametric_t<float32_t, float32_t>;
// the protocols
using product_t = pyre::flow::product_t;
using product_ref_t = pyre::flow::product_ref_t;
// intervals
using interval_t = pyre::flow::interval_t;


// check that no stale product among {products} has a fresh product right downstream of it,
// which, applied to every product of a graph, means none has a fresh product anywhere downstream
auto
consistent(const std::vector<product_ref_t> & products) -> bool
{
    // go through the products
    for (const auto & product : products) {
        // skip the fresh ones
        if (!product->stale()) {
            // on to the next
            continue;
        }
        // go through the factories that read a stale one
        for (const auto & [slot, reader] : product->readers()) {
            // that are still around
            auto factory = reader.lock();
            // skipping the ones that are gone
            if (!factory) {
                // on to the next
                continue;
            }
            // go through what they make
            for (const auto & [name, output] : factory->outputs()) {
                // a fresh one breaks the rule
                if (!output->stale()) {
                    // so say so
                    return false;
                }
            }
        }
    }
    // all good
    return true;
}


// driver
int
main(int argc, char * argv[])
{
    // the shape of the tiles
    auto shape = shape_t { 4, 4 };
    // the products
    auto signal = complex64_t::create("signal", shape, {});
    auto magnitude = float64_t::create("magnitude", shape, 0.0);
    auto normalized = float32_t::create("normalized", shape, 0.0f);
    auto red = float32_t::create("red", shape, 0.0f);
    auto green = float32_t::create("green", shape, 0.0f);
    auto blue = float32_t::create("blue", shape, 0.0f);
    auto image = image_t::create("image", shape);
    // all of them
    auto products =
        std::vector<product_ref_t> { signal, magnitude, normalized, red, green, blue, image };

    // a product starts fresh exactly when what it was made with is meaningful: a tile filled with
    // a value holds that value
    assert(!signal->stale());
    // while one whose cells were left uninitialized holds nothing yet
    assert(float32_t::create("blank", shape)->stale());

    // the factories, wired one slot at a time, checking the rule after every binding
    auto selector = selector_t::create("amplitude");
    selector->signal(signal);
    assert(consistent(products));
    selector->amplitude(magnitude);
    assert(consistent(products));
    // becoming the output of a factory makes a product stale, since its contents are not the
    // factory's yet
    assert(magnitude->stale());
    auto normalizer = normalizer_t::create("normalizer", { 0, 10 });
    normalizer->signal(magnitude);
    assert(consistent(products));
    normalizer->normalized(normalized);
    assert(consistent(products));
    auto colormap = colormap_t::create("gray");
    colormap->data(normalized);
    colormap->red(red);
    colormap->green(green);
    colormap->blue(blue);
    assert(consistent(products));
    auto codec = codec_t::create("bmp");
    codec->red(red);
    codec->green(green);
    codec->blue(blue);
    codec->image(image);
    assert(consistent(products));

    // writing the signal
    auto & cells = signal->write();
    // cell by cell
    for (int cell = 0; cell < 16; ++cell) {
        // with magnitudes 0, 1, 2, ...
        cells[cell] = std::polar(static_cast<float>(cell), 0.1f * cell);
    }
    // left everything downstream stale
    assert(image->stale());
    assert(consistent(products));
    // pull the image
    image->read();
    // which is fresh now
    assert(!image->stale());
    assert(consistent(products));

    // a new setting
    normalizer->interval(interval_t { 0, 20 });
    // makes everything downstream of the normalizer stale
    assert(normalized->stale() && image->stale());
    // but nothing upstream
    assert(!magnitude->stale());
    assert(consistent(products));
    // pull again
    image->read();
    assert(consistent(products));

    // a new value for every cell of the signal
    signal->value({ 1.0f, 0.0f });
    // leaves the signal fresh, since it holds exactly that
    assert(!signal->stale());
    // and everything downstream stale
    assert(image->stale());
    assert(consistent(products));
    // pull again
    image->read();

    // a replacement for the signal, bound through the typed setter
    auto other = complex64_t::create("other", shape, { 2.0f, 0.0f });
    selector->removeInput("signal");
    // undoing the binding flushes nothing
    assert(!image->stale());
    // binding the replacement flushes the selector
    selector->signal(other);
    assert(magnitude->stale() && image->stale());
    // and a pull reaches the new signal
    image->read();
    assert(std::abs(red->read()[0] - 0.1f) < 1e-6f);
    // the replacement joins the products of the graph
    products.push_back(other);
    assert(consistent(products));

    // a normalizer that loses its input keeps what it computed
    normalizer->removeInput("signal");
    assert(!image->stale());
    // but once something asks it to recompute
    normalizer->interval(interval_t { 0, 10 });
    assert(image->stale());
    // the pull fails, quietly here
    pyre::journal::error_t::quiet();
    // by raising
    try {
        // pull the image
        image->read();
        // so we can't get here
        assert(false);
    } catch (const pyre::journal::application_error &) {
        // as expected
    }
    // which leaves the normalized values stale
    assert(normalized->stale());
    // and the rule intact
    assert(consistent(products));

    // a loop: a filter that reads its own output
    auto looped = float32_t::create("looped", shape, 0.5f);
    auto loop = loop_t::create("loop");
    // bound both ways
    loop->signal(looped);
    loop->normalized(looped);
    // flushes in finite time, since the flush stops where it has been
    loop->flush();
    // and leaves the tile stale
    assert(looped->stale());

    // all done
    return 0;
}


// end of file
