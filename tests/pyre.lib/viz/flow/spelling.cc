// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// check that the products and the factories of the amplitude pipeline spell their types the same
// way on every compiler, since a catalog files them under these spellings


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
// a tile over cells of a given type
template <typename cellT>
using tile_t =
    pyre::flow::products::tile_t<pyre::grid::grid_t<packing_t, pyre::memory::heap_t<cellT>>>;
// the tiles of the pipeline
using complex64_t = tile_t<std::complex<float>>;
using float64_t = tile_t<double>;
using float32_t = tile_t<float>;
// the encoded image
using image_t = pyre::viz::products::images::bmp_t;
// the factories
using amplitude_t = pyre::flow::factories::selectors::amplitude_t<complex64_t, float64_t>;
using normalizer_t = pyre::flow::factories::filters::parametric_t<float64_t, float32_t>;
using colormap_t = pyre::viz::factories::colormaps::gray_t<float32_t>;
using codec_t = pyre::viz::factories::codecs::bmp_t<float32_t>;


// driver
int
main(int argc, char * argv[])
{
    // the spelling of the tiles over each cell type
    const auto complex64 =
        "pyre::flow::products::tile_t<pyre::grid::grid_t<"
        "pyre::grid::canonical_t<2>, "
        "pyre::memory::heap_t<std::complex<float>>>>";
    const auto float64 =
        "pyre::flow::products::tile_t<pyre::grid::grid_t<"
        "pyre::grid::canonical_t<2>, pyre::memory::heap_t<double>>>";
    const auto float32 =
        "pyre::flow::products::tile_t<pyre::grid::grid_t<"
        "pyre::grid::canonical_t<2>, pyre::memory::heap_t<float>>>";
    // a tile spells its declaration with the one of its grid
    assert(complex64_t::declSelf() == complex64);
    assert(float64_t::declSelf() == float64);
    assert(float32_t::declSelf() == float32);
    // and its readable name with the name of its grid
    assert(float64_t::className() == "TileGridCanonical2DHeapDouble");
    // the image spells its own
    assert(image_t::declSelf() == "pyre::viz::products::images::bmp_t");
    assert(image_t::className() == "BMP");

    // a factory spells its declaration with the ones of the products it takes, in order, with
    // every template parameter spelled out
    assert(
        amplitude_t::declSelf()
        == std::string("pyre::flow::factories::selectors::amplitude_t<") + complex64 + ", "
               + float64 + ">");
    assert(
        normalizer_t::declSelf()
        == std::string("pyre::flow::factories::filters::parametric_t<") + float64 + ", " + float32
               + ">");
    assert(
        colormap_t::declSelf()
        == std::string("pyre::viz::factories::colormaps::gray_t<") + float32 + ", " + float32 + ", "
               + float32 + ", " + float32 + ">");
    assert(
        codec_t::declSelf()
        == std::string("pyre::viz::factories::codecs::bmp_t<") + float32 + ", " + float32 + ", "
               + float32 + ">");
    // and its readable name is its kind
    assert(amplitude_t::className() == "Amplitude");
    assert(normalizer_t::className() == "Parametric");
    assert(colormap_t::className() == "Gray");
    assert(codec_t::className() == "BMP");

    // all done
    return 0;
}


// end of file
