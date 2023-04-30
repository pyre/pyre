// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// STL
#include <vector>
#include <fstream>
// support
#include <pyre/viz.h>


// type aliases
// the data type
using data_t = std::complex<double>;
// a container to put them in
using dataset_t = std::vector<data_t>;
// and an iterator over it
using cursor_t = dataset_t::const_iterator;

// my filter
using amplitude_t = pyre::viz::filters::logsaw_t<cursor_t>;
// my color map
using graymap_t = pyre::viz::colormaps::gray_t<amplitude_t>;

// the workflow terminal
using bmp_t = pyre::viz::bmp_t;
// and a stream to write it into
using ofstream_t = pyre::viz::ofstream_t;


// driver
int
main(int argc, char * argv[])
{
    // we are discretizing the unit square centered at the origin
    // for a given number of bins
    const int bins = 1001;
    // the spacing is
    const double delta = 4.0 / (bins - 1);

    // make a dataset
    dataset_t data;
    // with enough room
    data.reserve(bins * bins);
    // go through it
    for (int i = 0; i < bins; ++i) {
        for (int j = 0; j < bins; ++j) {
            // convert the indices into a complex number in our space
            data_t z { -2.0 + j * delta, 2.0 - i * delta };
            // compute f(z)
            auto f = (z - 1.0) / (z * z + z + 1.0);
            // place into the data set
            data.emplace(data.end(), f);
        }
    }

    // set up the workflow
    // point to the beginning of the data
    auto start = data.begin();
    // make an amplitude filter
    auto filter = amplitude_t(start);
    // make a color map
    graymap_t colormap(filter);
    // make a bitmap
    bmp_t bmp(bins, bins);
    // connect it to the color map
    const char * img = reinterpret_cast<char *>(bmp.encode(colormap));

    // open a file
    ofstream_t str("logsaw.bmp", std::ios::out | std::ios::binary);
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
