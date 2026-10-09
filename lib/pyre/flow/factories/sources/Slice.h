// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "forward.h"
// my superclass
#include "../../protocols/Factory.h"


// copy a window of a raster into a tile: the cell at {row, column} of the tile is the cell of the
// raster at {(origin + {row, column}) * stride}, so {origin} is counted in strides, the way a
// viewer counts tiles at a zoom level; the shape of the window is the shape of the tile, fixed
// when the tile is made, while {origin} and {stride} change with every request
template <class sourceT, class sliceT>
class pyre::flow::factories::sources::Slice : public pyre::flow::protocols::Factory {
    // type aliases
public:
    // me
    using self_type = Slice<sourceT, sliceT>;
    // my superclass
    using super_type = pyre::flow::protocols::Factory;
    // my slots
    using source_type = sourceT;
    using slice_type = sliceT;
    // the location of the window, and the distance between the cells it samples, per axis
    using pair_type = pair_t;
    // the spelling of types
    using string_type = string_t;

    // ref to me
    using factory_ref_type = std::shared_ptr<Slice>;
    // and to my products
    using source_ref_type = std::shared_ptr<source_type>;
    using slice_ref_type = std::shared_ptr<slice_type>;

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
    inline static auto create(
        const name_type & name = "", pair_type origin = { 0, 0 }, pair_type stride = { 1, 1 })
        -> factory_ref_type;

    // metamethods
public:
    // destructor
    inline virtual ~Slice();
    // constructor; DON'T CALL
    inline Slice(sentinel_type, const name_type &, pair_type, pair_type);

    // accessors
public:
    // the location of the window, counted in strides
    inline auto origin() const -> pair_type;
    // the distance between the cells of the raster the window samples, per axis
    inline auto stride() const -> pair_type;
    // the product bound to my {source} slot
    inline auto source() -> source_ref_type;
    // the product bound to my {slice} slot
    inline auto slice() -> slice_ref_type;

    // mutators
public:
    // move the window
    inline auto origin(pair_type) -> factory_ref_type;
    // change the distance between the cells it samples
    inline auto stride(pair_type) -> factory_ref_type;
    // bind my {source} slot
    inline auto source(source_ref_type) -> factory_ref_type;
    // bind my {slice} slot
    inline auto slice(slice_ref_type) -> factory_ref_type;

    // flow protocol
public:
    inline virtual auto make(const name_type & slot, super_type::product_ref_type product)
        -> super_type::factory_ref_type override;

    // implementation details - data
private:
    // the location of the window, counted in strides
    pair_type _origin;
    // the distance between the cells it samples
    pair_type _stride;

    // suppressed metamethods
private:
    // constructors
    Slice(const Slice &) = delete;
    Slice & operator=(const Slice &) = delete;
    Slice(Slice &&) = delete;
    Slice & operator=(Slice &&) = delete;
};

// get the inline definitions
#include "Slice.icc"


// end of file
