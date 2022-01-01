// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2022 all rights reserved


// STL
#include <vector>
#include <fstream>
// support
#include <pyre/viz.h>


// type aliases
using bmp_t = pyre::viz::bmp_t;
using color_t = pyre::viz::color_t;

// driver
int
main(int argc, char * argv[])
{
    // pick a height
    int height = 255;
    // and a width
    int width = 255;

    // make a vector of {rgb} triplets
    std::vector<bmp_t::rgb_type> data;
    // give it enough room
    data.reserve(width * height);
    // go through it
    for (auto idx = 0; idx < width * height; ++idx) {
        // form the colors
        color_t c = (idx % 256) / 255.;
        // and place color values
        data.emplace(data.end(), c / 2, 3 * c / 4, c);
    }

    // make a bitmap
    bmp_t bmp(height, width);

    // point to the beginning of the data
    auto start = data.begin();
    // encode
    auto img = bmp.encode(start);

    // open a file
    std::ofstream str("chip.bmp", std::ios::out | std::ios::binary);
    // if we succeeded
    if (str.is_open()) {
        // ask for the stream size
        auto bytes = bmp.bytes();
        // write
        str.write(img, bytes);
    }

    // all done
    return 0;
}


// end of file
