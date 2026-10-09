// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "forward.h"
#include "../../products/images/BMP.h"

// encode three color channels into a microsoft bitmap
template <class redT, class greenT, class blueT>
class pyre::viz::factories::codecs::BMP : public pyre::flow::factory_t {
    // type aliases
public:
    // me
    using self_type = BMP<redT, greenT, blueT>;
    // my superclass
    using super_type = pyre::flow::factory_t;
    // my input slots
    using red_type = redT;
    using green_type = greenT;
    using blue_type = blueT;
    // my output slot
    using image_type = pyre::viz::products::images::BMP;

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

    // the spelling of types
    using string_type = string_t;

    // the spelling of my type, and the descriptions of my slots and settings
public:
    // simulate my c++ declaration
    static inline auto declSelf() -> string_type;
    // the human readable form of my class name
    static inline auto className() -> string_type;
    // the descriptions of my slots, shared by every factory of my type
    static inline auto declSlots() -> const slots_type &;
    // the descriptions of my settings, shared by every factory of my type
    static inline auto declSettings() -> const settings_type &;

    // introspection
public:
    // the descriptions of my slots
    inline virtual auto slots() const -> const slots_type & override;
    // the descriptions of my settings
    inline virtual auto settings() const -> const settings_type & override;

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
    inline virtual auto make(const name_type & slot, super_type::product_ref_type product)
        -> super_type::factory_ref_type override;

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
