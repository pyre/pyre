// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// STL
#include <vector>
#include <fstream>
// support
#include <pyre/grid.h>
#include <pyre/viz.h>


// type aliases
// the data type
using data_t = std::complex<double>;
// storage
using storage_t = pyre::memory::heap_t<data_t>;
// layout
using packing_t = pyre::grid::canonical_t<2>;
// the container to put them in
using dataset_t = pyre::grid::grid_t<packing_t, storage_t>;
// indices
using index_t = dataset_t::index_type;
// shapes
using shape_t = dataset_t::shape_type;


// my filters
using decimate_t = pyre::viz::filters::decimate_t<dataset_t>;
using phase_t = pyre::viz::filters::phase_t<decimate_t>;
using mag_t = pyre::viz::filters::logsaw_t<decimate_t>;
using pol_t = pyre::viz::filters::polarsaw_t<phase_t>;
using mul_t = pyre::viz::filters::mul_t<mag_t, pol_t>;
// my color map
using hl_t = pyre::viz::colormaps::hl_t<phase_t, mul_t>;

// the workflow terminal
using bmp_t = pyre::viz::bmp_t;
// and a stream to write it into
using ofstream_t = pyre::viz::ofstream_t;


// driver
int
main(int argc, char * argv[])
{
    // a scale
    auto k = 1 << 10;
    // the dataset shape
    shape_t shape { 4 * k, 4 * k };
    // use canonical packing
    packing_t layout { shape };
    // the spacing
    auto deltaX = 4.0 / (shape[0] - 1);
    auto deltaY = 4.0 / (shape[1] - 1);

    // instantiate the dataset
    dataset_t data { layout, layout.cells() };
    // traverse in layout order
    for (auto idx : data.layout()) {
        // unpack
        auto [i, j] = idx;
        // convert the indices into a complex number in our space
        data_t z { -2.0 + j * deltaX, 2.0 - i * deltaY };
        // compute f(z)
        auto f = (z - 1.0) / (z * z + z + 1.0);
        // place into the data set
        data[idx] = f;
    }

    // set up a scale
    int scale = 4;
    // turn it into a shift
    index_t stride { scale };
    // make the decimator
    decimate_t decimator { data, layout.origin(), shape, stride };

    // make a phase filter for the hue
    auto hue = phase_t(decimator);
    // log sawtooth for the brightness
    auto bright = mul_t(mag_t(decimator), pol_t(hue));
    // make a color map
    hl_t colormap(hue, bright);
    // make a bitmap
    bmp_t bmp(shape[0] / scale, shape[1] / scale);
    // connect it to the color map
    const char * img = reinterpret_cast<char *>(bmp.encode(colormap));

    // open a file
    ofstream_t str("decimate.bmp", std::ios::out | std::ios::binary);
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
