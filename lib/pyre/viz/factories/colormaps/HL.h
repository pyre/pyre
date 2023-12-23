// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#pragma once

// encode three color channels into a microsoft bitmap
class pyre::viz::factories::colormaps::HL : public pyre::flow::factory_t {
    // type aliases
public:
    // my base class
    using base_type = pyre::flow::factory_t;
    // my slots
    using channel_type = pyre::viz::products::memory::tile_f4_t;

    // ref to me
    using factory_ref_type = std::shared_ptr<HL>;
    // my input slots
    using channel_ref_type = std::shared_ptr<channel_type>;

    // factory
public:
    inline static auto create(double threshold = 0.4) -> factory_ref_type;

    // metamethods
public:
    // destructor
    virtual ~HL();
    // constructor: DON'T CALL
    inline HL(sentinel_type, double);

    // accessors
public:
    // input slots
    auto hue() -> channel_ref_type;
    auto luminosity() -> channel_ref_type;
    // output slots
    auto red() -> channel_ref_type;
    auto green() -> channel_ref_type;
    auto blue() -> channel_ref_type;

    // mutators
public:
    // input slots
    auto hue(channel_ref_type) -> factory_ref_type;
    auto luminosity(channel_ref_type) -> factory_ref_type;
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