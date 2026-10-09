// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "forward.h"

// map perceptual lightness, chroma, and hue onto the three color channels
template <class lightnessT, class chromaT, class hueT, class redT, class greenT, class blueT>
class pyre::viz::factories::colormaps::OKLCH : public pyre::flow::factory_t {
    // type aliases
public:
    // me
    using self_type = OKLCH<lightnessT, chromaT, hueT, redT, greenT, blueT>;
    // my superclass
    using super_type = pyre::flow::factory_t;
    // my input slots
    using lightness_type = lightnessT;
    using chroma_type = chromaT;
    using hue_type = hueT;
    // my output slots
    using red_type = redT;
    using green_type = greenT;
    using blue_type = blueT;

    // ref to me
    using factory_ref_type = std::shared_ptr<OKLCH>;
    // and my slots
    using lightness_ref_type = std::shared_ptr<lightness_type>;
    using chroma_ref_type = std::shared_ptr<chroma_type>;
    using hue_ref_type = std::shared_ptr<hue_type>;
    using red_ref_type = std::shared_ptr<red_type>;
    using green_ref_type = std::shared_ptr<green_type>;
    using blue_ref_type = std::shared_ptr<blue_type>;

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
    virtual ~OKLCH();
    // constructor: DON'T CALL
    inline OKLCH(sentinel_type, const name_type &);

    // accessors
public:
    // input slots
    auto lightness() -> lightness_ref_type;
    auto chroma() -> chroma_ref_type;
    auto hue() -> hue_ref_type;
    // output slots
    auto red() -> red_ref_type;
    auto green() -> green_ref_type;
    auto blue() -> blue_ref_type;

    // mutators
public:
    // input slots
    auto lightness(lightness_ref_type) -> factory_ref_type;
    auto chroma(chroma_ref_type) -> factory_ref_type;
    auto hue(hue_ref_type) -> factory_ref_type;
    // output slots
    auto red(red_ref_type) -> factory_ref_type;
    auto green(green_ref_type) -> factory_ref_type;
    auto blue(blue_ref_type) -> factory_ref_type;

    // flow protocol
public:
    virtual auto make(const name_type & slot, super_type::product_ref_type product)
        -> super_type::factory_ref_type override;

    // suppressed metamethods
private:
    // constructors
    OKLCH(const OKLCH &) = delete;
    OKLCH & operator=(const OKLCH &) = delete;
    OKLCH(OKLCH &&) = delete;
    OKLCH & operator=(OKLCH &&) = delete;
};

// get the inline definitions
#include "OKLCH.icc"


// end of file
