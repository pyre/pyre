// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2024 all rights reserved

// code guard
#pragma once

// encode three color channels into a microsoft bitmap
template <class hueT, class saturationT, class luminosityT, class redT, class greenT, class blueT>
class pyre::viz::factories::colormaps::HSL : public pyre::flow::factory_t {
    // type aliases
public:
    // my base class
    using base_type = pyre::flow::factory_t;
    // my input slots
    using hue_type = hueT;
    using saturation_type = saturationT;
    using luminosity_type = luminosityT;
    // my output slots
    using red_type = redT;
    using green_type = greenT;
    using blue_type = blueT;

    // ref to me
    using factory_ref_type = std::shared_ptr<HSL>;
    // and my slots
    using hue_ref_type = std::shared_ptr<hue_type>;
    using saturation_ref_type = std::shared_ptr<saturation_type>;
    using luminosity_ref_type = std::shared_ptr<luminosity_type>;
    using red_ref_type = std::shared_ptr<red_type>;
    using green_ref_type = std::shared_ptr<green_type>;
    using blue_ref_type = std::shared_ptr<blue_type>;

    // factory
public:
    inline static auto create(const name_type & name = "") -> factory_ref_type;

    // metamethods
public:
    // destructor
    virtual ~HSL();
    // constructor: DON'T CALL
    inline HSL(sentinel_type, const name_type &);

    // accessors
public:
    // input slots
    auto hue() -> hue_ref_type;
    auto saturation() -> saturation_ref_type;
    auto luminosity() -> luminosity_ref_type;
    // output slots
    auto red() -> red_ref_type;
    auto green() -> green_ref_type;
    auto blue() -> blue_ref_type;

    // mutators
public:
    // input slots
    auto hue(hue_ref_type) -> factory_ref_type;
    auto saturation(saturation_ref_type) -> factory_ref_type;
    auto luminosity(luminosity_ref_type) -> factory_ref_type;
    // output slots
    auto red(red_ref_type) -> factory_ref_type;
    auto green(green_ref_type) -> factory_ref_type;
    auto blue(blue_ref_type) -> factory_ref_type;

    // flow protocol
public:
    virtual auto make(const name_type & slot, base_type::product_ref_type product)
        -> base_type::factory_ref_type override;

    // suppressed metamethods
private:
    // constructors
    HSL(const HSL &) = delete;
    HSL & operator=(const HSL &) = delete;
    HSL(HSL &&) = delete;
    HSL & operator=(HSL &&) = delete;
};

// get the inline definitions
#include "HSL.icc"

// end of file