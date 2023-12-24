// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#pragma once

// encode three color channels into a microsoft bitmap
class pyre::viz::factories::colormaps::Gray : public pyre::flow::factory_t {
    // type aliases
public:
    // my base class
    using base_type = pyre::flow::factory_t;
    // my slots
    using channel_type = pyre::viz::products::memory::tile_f4_t;

    // ref to me
    using factory_ref_type = std::shared_ptr<Gray>;
    // my input slots
    using channel_ref_type = std::shared_ptr<channel_type>;

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
    auto data() -> channel_ref_type;
    // output slots
    auto red() -> channel_ref_type;
    auto green() -> channel_ref_type;
    auto blue() -> channel_ref_type;

    // mutators
public:
    // input slot
    auto data(channel_ref_type) -> factory_ref_type;
    // output slots
    auto red(channel_ref_type) -> factory_ref_type;
    auto green(channel_ref_type) -> factory_ref_type;
    auto blue(channel_ref_type) -> factory_ref_type;

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