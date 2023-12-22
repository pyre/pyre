// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#pragma once

// encode three color channels into a microsoft bitmap
class pyre::viz::factories::codecs::BMP : public pyre::flow::factory_t {
    // type aliases
public:
    // my base class
    using base_type = pyre::flow::factory_t;
    // my input slots
    using channel_type = pyre::viz::products::memory::tile_f4_t;
    // my output slot
    using image_type = pyre::viz::products::images::bmp_t;

    /// the pixel type
    using pixel_type = image_type::cell_type;

    // ref to me
    using factory_ref_type = std::shared_ptr<BMP>;
    // my input slots
    using channel_ref_type = std::shared_ptr<channel_type>;
    // and output slots
    using image_ref_type = std::shared_ptr<image_type>;

    // factory
public:
    inline static auto create() -> factory_ref_type;

    // metamethods
public:
    // destructor
    virtual ~BMP();
    // constructor: DON'T CALL
    inline BMP(sentinel_type);

    // accessors
public:
    auto red() -> channel_ref_type;
    auto green() -> channel_ref_type;
    auto blue() -> channel_ref_type;
    auto image() -> image_ref_type;

    // mutators
public:
    auto red(channel_ref_type) -> factory_ref_type;
    auto green(channel_ref_type) -> factory_ref_type;
    auto blue(channel_ref_type) -> factory_ref_type;
    auto image(image_ref_type) -> factory_ref_type;

    // flow protocol
public:
    virtual auto make(name_type slot, base_type::product_ref_type product)
        -> base_type::factory_ref_type override;

    // suppressed metamethods
private:
    // constructors
    BMP(const BMP &) = delete;
    BMP & operator=(const BMP &) = delete;
    BMP(BMP &&) = delete;
    BMP & operator=(BMP &&) = delete;
};

// get the inline definitions
#include "BMP.icc"

// end of file
