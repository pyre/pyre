// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// interpret three input sources as {hue, saturation, luminosity} and generate {rgb_t} color
template <class lightnessSourceT, class chromaSourceT, class hueSourceT>
class pyre::viz::iterators::colormaps::OKLCH {
    // types
public:
    // my template parameters
    using lightness_source_type = lightnessSourceT;
    using chroma_source_type = chromaSourceT;
    using hue_source_type = hueSourceT;
    // and their reference types
    using lightness_source_const_reference = const lightness_source_type &;
    using chroma_source_const_reference = const chroma_source_type &;
    using hue_source_const_reference = const hue_source_type &;

    // i generate {r,g,b} triplets
    using rgb_type = viz::rgb_t;

    // metamethods
public:
    inline OKLCH(
        lightness_source_const_reference, chroma_source_const_reference,
        hue_source_const_reference);

    // interface: pretend to be an iterator
public:
    // map the current data value to a color
    inline auto operator*() const -> rgb_type;
    // get the next value from the source; only support the prefix form, if possible
    inline auto operator++() -> void;

    // implementation details: data
private:
    // the data source
    lightness_source_type _lightness;
    chroma_source_type _chroma;
    hue_source_type _hue;

    // default metamethods
public:
    // destructor
    ~OKLCH() = default;

    // constructors
    OKLCH(const OKLCH &) = default;
    OKLCH(OKLCH &&) = default;
    OKLCH & operator=(const OKLCH &) = default;
    OKLCH & operator=(OKLCH &&) = default;
};


// get the inline definitions
#include "OKLCH.icc"


// end of file
