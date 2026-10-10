// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// check that every factory that describes itself names its slots and settings the way python
// names them, in order, with the right directions and types


// portability
#include <portinfo>
// STL
#include <cassert>
#include <complex>
#include <string>
#include <utility>
#include <vector>
// support
#include <pyre/viz.h>


// type aliases
// all tiles are two dimensional
using packing_t = pyre::grid::canonical_t<2>;
// a tile over cells of a given type
template <typename cellT>
using tile_t =
    pyre::flow::products::tile_t<pyre::grid::grid_t<packing_t, pyre::memory::heap_t<cellT>>>;
// the tiles
using complex_t = tile_t<std::complex<double>>;
using real_t = tile_t<double>;
// the namespaces of the factories
namespace selectors = pyre::flow::factories::selectors;
namespace filters = pyre::flow::factories::filters;
namespace sources = pyre::flow::factories::sources;
namespace colormaps = pyre::viz::factories::colormaps;
namespace codecs = pyre::viz::factories::codecs;
// the expected slots: name, and whether the factory reads it
using slots_t = std::vector<std::pair<std::string, bool>>;
// the expected settings: name, and type
using settings_t = std::vector<std::pair<std::string, std::string>>;


// check that the factories of type {factoryT} describe the {slots} and {settings}
template <class factoryT>
auto
check(const slots_t & slots, const settings_t & settings) -> void
{
    // the descriptions of the slots
    const auto & declared = factoryT::declSlots();
    // as many as expected
    assert(declared.size() == slots.size());
    // go through them
    for (std::size_t index = 0; index < slots.size(); ++index) {
        // the name
        assert(declared[index].name() == slots[index].first);
        // and the direction
        assert(declared[index].reads() == slots[index].second);
    }
    // the descriptions of the settings
    const auto & described = factoryT::declSettings();
    // as many as expected
    assert(described.size() == settings.size());
    // go through them
    for (std::size_t index = 0; index < settings.size(); ++index) {
        // the name
        assert(described[index].name() == settings[index].first);
        // and the type
        assert(described[index].type() == settings[index].second);
    }
    // all done
    return;
}


// driver
int
main(int argc, char * argv[])
{
    // the slot that reads a signal
    const auto signal = std::pair<std::string, bool> { "signal", true };
    // the color channels a colormap writes
    const auto rgb = slots_t { { "red", false }, { "green", false }, { "blue", false } };

    // selectors
    check<selectors::amplitude_t<complex_t, real_t>>({ signal, { "amplitude", false } }, {});
    check<selectors::imaginary_t<complex_t, real_t>>({ signal, { "imaginary", false } }, {});
    check<selectors::phase_t<complex_t, real_t>>({ signal, { "phase", false } }, {});
    check<selectors::real_t<complex_t, real_t>>({ signal, { "real", false } }, {});

    // filters
    check<filters::affine_t<real_t, real_t>>(
        { signal, { "affine", false } }, { { "interval", "interval" } });
    check<filters::constant_t<real_t>>({ { "tile", false } }, { { "value", "double" } });
    check<filters::constant_t<complex_t>>({ { "tile", false } }, {});
    check<filters::cycle_t<complex_t, real_t>>(
        { signal, { "cycle", false } }, { { "interval", "interval" } });
    check<filters::decimate_t<real_t>>({ signal, { "decimated", false } }, { { "level", "int" } });
    check<filters::geometric_t<real_t, real_t>>({ signal, { "bin", false } }, {});
    check<filters::logsaw_t<real_t, real_t>>({ signal, { "logsaw", false } }, {});
    check<filters::parametric_t<real_t, real_t>>(
        { signal, { "normalized", false } }, { { "interval", "interval" } });
    check<filters::polarsaw_t<complex_t, real_t>>({ signal, { "polarsaw", false } }, {});
    check<filters::power_t<real_t, real_t>>(
        { signal, { "power", false } },
        { { "mean", "double" }, { "scale", "double" }, { "exponent", "double" } });
    check<filters::uniform_t<real_t, real_t>>({ signal, { "bin", false } }, { { "bins", "int" } });

    // sources
    check<sources::slice_t<real_t, real_t>>(
        { { "source", true }, { "slice", false } }, { { "origin", "pair" }, { "stride", "pair" } });

    // colormaps
    // the slots of a colormap that reads {inputs}
    auto colormap = [&rgb](slots_t inputs) -> slots_t {
        // followed by the color channels
        inputs.insert(inputs.end(), rgb.begin(), rgb.end());
        // hand them off
        return inputs;
    };
    check<colormaps::complex_t<complex_t, real_t, real_t, real_t>>(colormap({ signal }), {});
    check<colormaps::gray_t<real_t>>(colormap({ { "data", true } }), {});
    check<colormaps::hl_t<real_t>>(
        colormap({ { "hue", true }, { "luminosity", true } }), { { "threshold", "double" } });
    check<colormaps::hsb_t<real_t>>(
        colormap({ { "hue", true }, { "saturation", true }, { "brightness", true } }), {});
    check<colormaps::hsl_t<real_t>>(
        colormap({ { "hue", true }, { "saturation", true }, { "luminosity", true } }), {});
    check<colormaps::oklch_t<real_t>>(
        colormap({ { "lightness", true }, { "chroma", true }, { "hue", true } }), {});

    // codecs
    check<codecs::bmp_t<real_t>>(
        { { "red", true }, { "green", true }, { "blue", true }, { "image", false } }, {});

    // all done
    return 0;
}


// end of file
