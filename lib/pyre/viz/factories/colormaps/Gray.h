// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2024 all rights reserved

// code guard
#pragma once

// encode three color channels into a microsoft bitmap
template <class signalT, class redT, class greenT, class blueT>
class pyre::viz::factories::colormaps::Gray : public pyre::flow::factory_t {
    // type aliases
public:
    // my base class
    using base_type = pyre::flow::factory_t;
    // my slots
    using signal_type = signalT;
    using red_type = redT;
    using green_type = greenT;
    using blue_type = blueT;

    // ref to me
    using factory_ref_type = std::shared_ptr<Gray>;
    // and my slots
    using signal_ref_type = std::shared_ptr<signal_type>;
    using red_ref_type = std::shared_ptr<red_type>;
    using green_ref_type = std::shared_ptr<green_type>;
    using blue_ref_type = std::shared_ptr<blue_type>;

    // factory
public:
    inline static auto create(const name_type & = "") -> factory_ref_type;

    // metamethods
public:
    // destructor
    virtual ~Gray();
    // constructor: DON'T CALL
    inline Gray(sentinel_type, const name_type &);

    // accessors
public:
    // input slot
    auto data() -> signal_ref_type;
    // output slots
    auto red() -> red_ref_type;
    auto green() -> green_ref_type;
    auto blue() -> blue_ref_type;

    // mutators
public:
    // input slot
    auto data(signal_ref_type) -> factory_ref_type;
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
    Gray(const Gray &) = delete;
    Gray & operator=(const Gray &) = delete;
    Gray(Gray &&) = delete;
    Gray & operator=(Gray &&) = delete;
};

// get the inline definitions
#include "Gray.icc"

// end of file