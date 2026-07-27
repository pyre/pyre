// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// externals
#include "externals.h"
// forward declarations
#include "forward.h"

// base class
#include "Buffer.h"
// the borrowed access to individual pages
#include "View.h"


// a block of cells assembled out of fixed-size pages, each a separate allocation
// the pages materialize on demand: a fresh store owns nothing, and clients bring pages into
// existence one at a time, fill them, and declare what state they are in; this is the storage
// side of out-of-core workflows, where only the working set of a much larger product is ever
// in memory
// each page carries three state bits:
//   {resident}: the page has been allocated; residency is monotonic: pages are never evicted,
//               and a store is reclaimed by destroying it as a whole
//   {valid}: the client has deposited meaningful content; also monotonic, which is what makes
//            it safe to hand out zero-copy views of a page
//   {clean}: the content matches whatever backing store the client mirrors; writers taint the
//            pages they touch, and a flush marks them clean again, so scanning for dirty pages
//            is how a client finds out what needs saving
// there is no single expanse of memory here, so this strategy has no {data()}: it satisfies
// {StorageStrategy} but deliberately not {ContiguousStorage}
template <class T, bool isConst>
class pyre::memory::Paged : public Buffer<T, isConst> {
    // types
public:
    // me
    using self_type = Paged<T, isConst>;
    // my base class
    using super_type = Buffer<T, isConst>;

    // my cell
    using typename super_type::cell_type;
    // pull the type aliases
    using typename super_type::value_type;
    // derived types
    using typename super_type::pointer;
    using typename super_type::const_pointer;
    using typename super_type::reference;
    using typename super_type::const_reference;
    // distances
    using typename super_type::difference_type;
    // sizes of things
    using typename super_type::size_type;
    using typename super_type::cell_count_type;
    // my handle
    using typename super_type::handle_type;
    // strings
    using typename super_type::uri_type;
    using typename super_type::string_type;
    // the borrowed access to one of my pages
    using view_type = View<T, isConst>;

    // the record i keep for each page
    struct page_type {
        // the allocation; empty until the page becomes resident
        handle_type block {};
        // whether the client has deposited meaningful content
        bool valid { false };
        // whether the content has diverged from the client's backing store
        bool dirty { false };
    };
    // the page table
    using table_type = std::vector<page_type>;
    // held through a handle, so copies of me are views of the same store
    using table_handle_type = std::shared_ptr<table_type>;

    // metamethods
public:
    // build a store of {pages} pages of {pageCells} cells each, none of them resident
    inline Paged(cell_count_type pageCells, cell_count_type pages);

    // accessors
public:
    // human readable form of my location
    inline auto uri() const -> uri_type;
    // the number of cells i can hold: the full expanse, resident or not
    inline auto cells() const -> cell_count_type;
    // the memory footprint of the pages that are actually resident
    inline auto bytes() const -> size_type;
    // the number of cells in one page
    inline auto pageCells() const -> cell_count_type;
    // the number of pages
    inline auto pages() const -> cell_count_type;
    // how many of them are resident
    inline auto residents() const -> cell_count_type;

    // expose my constness
    static constexpr auto readonly() -> bool;
    static constexpr auto writable() -> bool;

    // simulate my c++ declaration
    static inline auto declSelf() -> string_type;
    // simulate the c++ declaration of my template parameter
    static inline auto declValue() -> string_type;
    // human readable name for my type
    static inline auto className() -> string_type;

    // page state
public:
    // whether a page has been allocated
    inline auto resident(cell_count_type) const -> bool;
    // whether the client has deposited meaningful content in it
    inline auto valid(cell_count_type) const -> bool;
    // whether its content matches the client's backing store
    inline auto clean(cell_count_type) const -> bool;

    // page management
public:
    // make a page resident, allocating it if this is its first use, and hand out its address
    inline auto reside(cell_count_type) const -> pointer;
    // record that the client has deposited meaningful content in a page
    inline auto validate(cell_count_type) const -> void;
    // record that the client has written to a page, so it diverges from the backing store
    inline auto taint(cell_count_type) const -> void;
    // record that the client has saved a page, so it matches the backing store again
    inline auto flush(cell_count_type) const -> void;
    // the address of a resident page
    inline auto page(cell_count_type) const -> pointer;
    // a borrowed view of a resident page, for wrapping in tile-shaped grids
    inline auto view(cell_count_type) const -> view_type;

    // data access
public:
    // with bounds and residency checking
    inline auto at(difference_type) const -> reference;
    // without checks, trusting the caller to reach only into resident pages
    inline auto operator[](difference_type) const -> reference;

    // implementation details: helpers
private:
    // guard a page ordinal, complaining and clamping when it reaches outside the table
    inline auto _verify(cell_count_type) const -> cell_count_type;

    // implementation details: data
private:
    // the number of cells in one page
    cell_count_type _pageCells;
    // the page table; through a handle, so copies of me share pages and their state
    table_handle_type _table;

    // default metamethods
public:
    // destructor
    ~Paged() = default;
    // constructors
    Paged(const Paged &) = default;
    Paged(Paged &&) = default;
    Paged & operator=(const Paged &) = default;
    Paged & operator=(Paged &&) = default;
};


// inline definitions
#include "Paged.icc"


// end of file
