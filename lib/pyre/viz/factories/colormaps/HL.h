// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2024 all rights reserved

// code guard
#pragma once

// encode three color channels into a microsoft bitmap
template <class hueT, class luminosityT, class redT, class greenT, class blueT>
class pyre::viz::factories::colormaps::HL : public pyre::flow::factory_t {
    // type aliases
public:
    // my base class
    using base_type = pyre::flow::factory_t;
    // my input slots
    using hue_type = hueT;
    using luminosity_type = luminosityT;
    // my output slots
    using red_type = redT;
    using green_type = greenT;
    using blue_type = blueT;

    // ref to me
    using factory_ref_type = std::shared_ptr<HL>;
    // and my slots
    using hue_ref_type = std::shared_ptr<hue_type>;
    using luminosity_ref_type = std::shared_ptr<luminosity_type>;
    using red_ref_type = std::shared_ptr<red_type>;
    using green_ref_type = std::shared_ptr<green_type>;
    using blue_ref_type = std::shared_ptr<blue_type>;

    // factory
public:
    inline static auto create(const name_type & name = "", double threshold = 0.4)
        -> factory_ref_type;

    // metamethods
public:
    // destructor
    virtual ~HL();
    // constructor: DON'T CALL
    inline HL(sentinel_type, const name_type &, double);

    // accessors
public:
    // input slots
    auto hue() -> hue_ref_type;
    auto luminosity() -> luminosity_ref_type;
    // output slots
    auto red() -> red_ref_type;
    auto green() -> green_ref_type;
    auto blue() -> blue_ref_type;

    // mutators
public:
    // input slots
    auto hue(hue_ref_type) -> factory_ref_type;
    auto luminosity(luminosity_ref_type) -> factory_ref_type;
    // output slots
    auto red(red_ref_type) -> factory_ref_type;
    auto green(green_ref_type) -> factory_ref_type;
    auto blue(blue_ref_type) -> factory_ref_type;

    // flow protocol
public:
    virtual auto make(const name_type & slot, base_type::product_ref_type product)
        -> base_type::factory_ref_type override;

    // implementation details
private:
    double _threshold;

    // suppressed metamethods
private:
    // constructors
    HL(const HL &) = delete;
    HL & operator=(const HL &) = delete;
    HL(HL &&) = delete;
    HL & operator=(HL &&) = delete;
};

// get the inline definitions
#include "HL.icc"

// end of file