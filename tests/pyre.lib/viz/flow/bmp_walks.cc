// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// portability
#include <portinfo>
// STL
#include <cassert>
#include <cstring>
#include <vector>
// support
#include <pyre/journal.h>
#include <pyre/timers.h>
#include <pyre/viz.h>


// type aliases
using cell_t = float;
using packing_t = pyre::grid::canonical_t<2>;
using storage_t = pyre::memory::heap_t<cell_t>;
using grid_t = pyre::grid::grid_t<packing_t, storage_t>;
using index_t = grid_t::index_type;
using shape_t = grid_t::shape_type;
using byte_t = unsigned char;
using walltimer_t = pyre::timers::wall_timer_t;


// the bytes of the pixel payload of a bitmap, line after line, each line padded to a multiple of
// four bytes; three ways to visit the cells of the color channels, which must agree

// through the grid iterators, which step through the packing
static auto
iterators(const grid_t & r, const grid_t & g, const grid_t & b, int padding, byte_t * out) -> void
{
    // unpack the shape
    auto [height, width] = r.packing().shape();
    // the cursors
    auto red = r.begin();
    auto green = g.begin();
    auto blue = b.begin();
    // go through the lines
    for (auto row = 0; row < height; ++row) {
        // and the pixels of each line
        for (auto column = 0; column < width; ++column) {
            // blue, green, and red, as the format wants them
            *out++ = static_cast<byte_t>(0xff * (*blue++));
            *out++ = static_cast<byte_t>(0xff * (*green++));
            *out++ = static_cast<byte_t>(0xff * (*red++));
        }
        // and the padding
        for (auto pad = 0; pad < padding; ++pad) {
            // with zeros
            *out++ = 0;
        }
    }
    // all done
    return;
}


// through the memory of the cells, in the order they are stored; this assumes row major tiles
static auto
memory(const grid_t & r, const grid_t & g, const grid_t & b, int padding, byte_t * out) -> void
{
    // unpack the shape
    auto [height, width] = r.packing().shape();
    // the first cell of each channel
    const cell_t * red = r.data();
    const cell_t * green = g.data();
    const cell_t * blue = b.data();
    // go through the lines
    for (auto row = 0; row < height; ++row) {
        // and the pixels of each line
        for (auto column = 0; column < width; ++column) {
            // blue, green, and red, as the format wants them
            *out++ = static_cast<byte_t>(0xff * (*blue++));
            *out++ = static_cast<byte_t>(0xff * (*green++));
            *out++ = static_cast<byte_t>(0xff * (*red++));
        }
        // and the padding
        for (auto pad = 0; pad < padding; ++pad) {
            // with zeros
            *out++ = 0;
        }
    }
    // all done
    return;
}


// through an index for each pixel, which the packing turns into an offset
static auto
indices(const grid_t & r, const grid_t & g, const grid_t & b, int padding, byte_t * out) -> void
{
    // unpack the shape
    auto [height, width] = r.packing().shape();
    // go through the lines
    for (auto row = 0; row < height; ++row) {
        // and the pixels of each line
        for (auto column = 0; column < width; ++column) {
            // the index of the pixel
            auto idx = index_t { row, column };
            // blue, green, and red, as the format wants them
            *out++ = static_cast<byte_t>(0xff * b[idx]);
            *out++ = static_cast<byte_t>(0xff * g[idx]);
            *out++ = static_cast<byte_t>(0xff * r[idx]);
        }
        // and the padding
        for (auto pad = 0; pad < padding; ++pad) {
            // with zeros
            *out++ = 0;
        }
    }
    // all done
    return;
}


// encode the channels of a tile of the given {shape} all three ways, check they agree, and time
// each one over {trials} encodings
static auto
compare(shape_t shape, int trials, pyre::journal::debug_t & report) -> void
{
    // unpack the shape
    auto [height, width] = shape;
    // the channels
    auto r = grid_t(packing_t(shape), shape.cells());
    auto g = grid_t(packing_t(shape), shape.cells());
    auto b = grid_t(packing_t(shape), shape.cells());
    // go through the cells
    for (auto row = 0; row < height; ++row) {
        // and the cells of each line
        for (auto column = 0; column < width; ++column) {
            // the index
            auto idx = index_t { row, column };
            // give each channel a pattern of its own, in [0,1]
            r[idx] = static_cast<cell_t>((row % 256) / 255.0);
            g[idx] = static_cast<cell_t>((column % 256) / 255.0);
            b[idx] = static_cast<cell_t>(((row + column) % 256) / 255.0);
        }
    }
    // the padding of a line
    auto padding = (4 - (width * 3) % 4) % 4;
    // the size of the payload
    auto size = height * (width * 3 + padding);
    // the three payloads
    auto viaIterators = std::vector<byte_t>(size);
    auto viaMemory = std::vector<byte_t>(size);
    auto viaIndices = std::vector<byte_t>(size);

    // the clocks
    auto iteratorClock = walltimer_t("pyre.viz.flow.bmp.walks.iterators");
    auto memoryClock = walltimer_t("pyre.viz.flow.bmp.walks.memory");
    auto indexClock = walltimer_t("pyre.viz.flow.bmp.walks.indices");
    // reset them
    iteratorClock.reset();
    memoryClock.reset();
    indexClock.reset();
    // go through the trials
    for (auto trial = 0; trial < trials; ++trial) {
        // through the iterators
        iteratorClock.start();
        iterators(r, g, b, padding, viaIterators.data());
        iteratorClock.stop();
        // through memory
        memoryClock.start();
        memory(r, g, b, padding, viaMemory.data());
        memoryClock.stop();
        // through indices
        indexClock.start();
        indices(r, g, b, padding, viaIndices.data());
        indexClock.stop();
    }

    // the three must agree
    assert(viaIterators == viaMemory);
    assert(viaIterators == viaIndices);

    // report the cost of one encoding, in milliseconds
    report
        // the tile
        << height << "x" << width
        << ": "
        // the iterators
        << "iterators " << iteratorClock.ms() / trials
        << ", "
        // memory
        << "memory " << memoryClock.ms() / trials
        << ", "
        // indices
        << "indices "
        << indexClock.ms() / trials
        // done with this tile
        << pyre::journal::newline;

    // all done
    return;
}


// compare three ways to visit the color channels while encoding a bitmap: the timings go to the
// debug channel {pyre.viz.flow.bmp.walks}, so the run is silent unless asked, e.g.
//     bmp_walks --journal.debug=pyre.viz.flow.bmp.walks
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("bmp_walks");
    // the channel for the timings
    auto report = pyre::journal::debug_t("pyre.viz.flow.bmp.walks");
    // the header
    report << pyre::journal::at() << "ms per encoding" << pyre::journal::newline;

    // a tile whose lines need padding, taller than it is wide
    compare(shape_t { 7, 5 }, 50, report);
    // and the tiles of a viewer
    compare(shape_t { 128, 128 }, 50, report);
    compare(shape_t { 256, 256 }, 50, report);
    compare(shape_t { 512, 512 }, 50, report);

    // flush the report
    report << pyre::journal::endl;

    // all done
    return 0;
}


// end of file
