// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_journal_Entry_h)
#define pyre_journal_Entry_h


// encapsulation of a journal message entry
class pyre::journal::Entry {
    // types
public:
    // aliases for myself
    using entry_type = Entry;
    using entry_reference = entry_type &;
    // the dent type
    using dent_type = dent_t;
    // message payload
    using page_type = page_t;
    using page_reference = page_type &;
    using page_const_reference = const page_type &;
    // message metadata
    using key_type = key_t;
    using value_type = value_t;
    using notes_type = notes_t;
    using notes_reference = notes_type &;
    using notes_const_reference = const notes_type &;
    // message buffering
    using line_type = line_t;
    using linebuf_type = linebuf_t;
    using linebuf_reference = linebuf_type &;
    // output streams
    using ostream_type = outputstream_t;

    // metamethods
public:
    // constructors
    inline explicit Entry();

    // interface
public:
    // accessors
    inline auto page() const -> page_const_reference;
    inline auto notes() const -> notes_const_reference;

    // mutators
    inline auto buffer() -> linebuf_reference;
    inline auto page() -> page_reference;
    inline auto notes() -> notes_reference;

    // transaction support
public:
    inline auto note(const key_type &, const value_type &) -> entry_reference;
    // move the buffer to the page and reset
    inline auto push(dent_type) -> entry_reference;
    // clear the page
    inline auto flush() -> entry_reference;

    // item injection
    template <typename itemT>
    inline void inject(const itemT &);

    // data
private:
    linebuf_type _buffer;
    page_type _page;
    notes_type _notes;

    // disallow
private:
    Entry(const Entry &) = delete;
    Entry(Entry &&) = delete;
    Entry & operator=(const Entry &) = delete;
    Entry & operator=(Entry &&) = delete;
};


// get the inline definitions
#define pyre_journal_Entry_icc
#include "Entry.icc"
#undef pyre_journal_Entry_icc


#endif

// end of file
