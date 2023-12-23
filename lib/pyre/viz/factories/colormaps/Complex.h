// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#pragma once

// encode three color channels into a microsoft bitmap
class pyre::viz::factories::colormaps::Complex : public pyre::flow::factory_t {
    // type aliases
public:
    // the {rgb} triplet
    using rgb_type = pyre::viz::rgb_t;

    // my base class
    using base_type = pyre::flow::factory_t;
    // my slots
    using channel_type = pyre::viz::products::memory::tile_f4_t;
    using signal_type = pyre::viz::products::memory::tile_c8_t;

    // ref to me
    using factory_ref_type = std::shared_ptr<Complex>;
    // and my slots
    using signal_ref_type = std::shared_ptr<signal_type>;
    using channel_ref_type = std::shared_ptr<channel_type>;

    // factory
public:
    inline static auto create(
        // color map configuration
        int bins = 32,
        // the amount of color to inject
        double saturation = 0.5,
        // brightness range
        double minBrightness = 0, double maxBrightness = 1,
        // the data space
        double minAmplitude = 0, double maxAmplitude = 1,
        // the colors to use for out of range data
        // by default, underflow maps to black
        rgb_type underflow = { 0, 0, 0 },
        // and overflow to white
        rgb_type overflow = { 1, 1, 1 }) -> factory_ref_type;

    // metamethods
public:
    // destructor
    virtual ~Complex();
    // constructor: DON'T CALL
    inline Complex(
        sentinel_type, int bins, double saturation, double minBrightness, double maxBrightness,
        double minAmplitude, double maxAmplitude, rgb_type underflow, rgb_type overflow);

    // accessors
public:
    // input slot
    auto signal() -> signal_ref_type;
    // output slots
    auto red() -> channel_ref_type;
    auto green() -> channel_ref_type;
    auto blue() -> channel_ref_type;

    // mutators
public:
    // input slots
    auto signal(signal_ref_type) -> factory_ref_type;
    // output slots
    auto red(channel_ref_type) -> factory_ref_type;
    auto green(channel_ref_type) -> factory_ref_type;
    auto blue(channel_ref_type) -> factory_ref_type;

    // flow protocol
public:
    virtual auto make(name_type slot, base_type::product_ref_type product)
        -> base_type::factory_ref_type override;

    // implementation details
private:
    int _bins;
    double _saturation;
    // hue mapping
    double _scaleHue;
    // brightness mapping
    double _minBrightness, _maxBrightness, _scaleBrightness;
    double _minAmplitude, _maxAmplitude, _scaleAmplitude;
    // out of range values
    rgb_type _overflow;
    rgb_type _underflow;

    // suppressed metamethods
private:
    // constructors
    Complex(const Complex &) = delete;
    Complex & operator=(const Complex &) = delete;
    Complex(Complex &&) = delete;
    Complex & operator=(Complex &&) = delete;
};

// get the inline definitions
#include "Complex.icc"

// end of file