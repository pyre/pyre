// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2024 all rights reserved

// code guard
#pragma once

// encode three color channels into a microsoft bitmap
template <class redT, class greenT, class blueT>
class pyre::viz::factories::codecs::BMP : public pyre::flow::factory_t {
    // type aliases
public:
    // my base class
    using base_type = pyre::flow::factory_t;
    // my input slots
    using red_type = redT;
    using green_type = greenT;
    using blue_type = blueT;
    // my output slot
    using image_type = pyre::viz::products::images::bmp_t;

    /// the pixel type
    using pixel_type = image_type::cell_type;

    // ref to me
    using factory_ref_type = std::shared_ptr<BMP>;
    // my input slots
    using red_ref_type = std::shared_ptr<red_type>;
    using green_ref_type = std::shared_ptr<green_type>;
    using blue_ref_type = std::shared_ptr<blue_type>;
    // and output slots
    using image_ref_type = std::shared_ptr<image_type>;

    // factory
public:
    inline static auto create(const name_type & name = "") -> factory_ref_type;

    // metamethods
public:
    // destructor
    inline virtual ~BMP();
    // constructor: DON'T CALL
    inline BMP(sentinel_type, const name_type &);

    // accessors
public:
    inline auto red() -> red_ref_type;
    inline auto green() -> green_ref_type;
    inline auto blue() -> blue_ref_type;
    inline auto image() -> image_ref_type;

    // mutators
public:
    inline auto red(red_ref_type) -> factory_ref_type;
    inline auto green(green_ref_type) -> factory_ref_type;
    inline auto blue(blue_ref_type) -> factory_ref_type;
    inline auto image(image_ref_type) -> factory_ref_type;

    // flow protocol
public:
    inline virtual auto make(const name_type & slot, base_type::product_ref_type product)
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
