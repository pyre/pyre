// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "forward.h"
// my superclass
#include "Device.h"


// a device that ships entries, as records, to another process over a file descriptor
//
// the far end of the descriptor is somebody else's concern: a parent process, a server, a
// daemon. this device never blocks and never raises: the descriptor is non-blocking, a record
// that cannot be written whole is dropped whole, drops are counted and reported once the far
// end catches up, and a far end that has gone away silences the courier
class pyre::journal::Courier : public Device {
    // types
public:
    // me
    using self_type = Courier;
    // pointers to me
    using pointer_type = std::shared_ptr<self_type>;
    // my superclass
    using super_type = Device;
    // the descriptor i write to
    using descriptor_type = int;
    // the device that also gets every entry
    using mirror_type = Device::pointer_type;
    // counters
    using count_type = size_t;
    // the wire form of a record
    using record_type = string_t;
    // the name of the sink an entry was delivered to
    using sink_type = string_t;

    // constants
public:
    // the channel on which drops are reported
    static constexpr const char * reporter = "journal.courier";

    // metamethods
public:
    // constructor
    explicit Courier(
        descriptor_type descriptor, const name_type & name = "courier",
        mirror_type mirror = nullptr);
    // destructor
    virtual ~Courier();

    // accessors
public:
    // the descriptor
    inline auto descriptor() const -> descriptor_type;
    // the device that also gets every entry
    inline auto mirror() const -> mirror_type;
    // the sequence number of the last record stamped
    inline auto seq() const -> count_type;
    // the number of records that made it out
    inline auto shipped() const -> count_type;
    // the number of records lost since the last successful write
    inline auto dropped() const -> count_type;
    // whether the far end has gone away
    inline auto dead() const -> bool;

    // interface
public:
    // user facing messages
    virtual auto alert(const entry_type &) -> Courier & override;
    // help screens
    virtual auto help(const entry_type &) -> Courier & override;
    // developer messages
    virtual auto memo(const entry_type &) -> Courier & override;
    // release the descriptor; nothing is delivered after this
    auto close() -> Courier &;

    // the pipeline
public:
    // convert an entry into a record and write it to the descriptor
    auto ship(const entry_type &) -> void;
    // render the record for an entry, with the origin stamped into its notes
    auto stamp(const entry_type &) -> record_type;
    // render the record that reports the entries dropped since the last successful write
    auto notice(const entry_type &) -> record_type;

    // implementation details
private:
    // hand an entry to the mirror, then ship it
    auto deliver(const entry_type &, const sink_type &) -> void;
    // account for an entry that never made it out
    auto lose() -> void;
    // attempt to finish writing the pending tail; report whether the descriptor is clear
    auto drain() -> bool;
    // write without blocking; report whether the descriptor accepted any of the data
    auto write(const record_type &) -> bool;
    // stamp the origin into a copy of the notes: the process, the given sequence number, the
    // time of the flush, and the host
    auto origin(const notes_t &, count_type) const -> notes_t;
    // render a record from its parts
    auto render(const page_t &, const notes_t &) const -> record_type;
    // render a string as a JSON literal
    static auto quote(const string_t &) -> string_t;

    // data
private:
    // the descriptor
    descriptor_type _descriptor;
    // the device that also gets every entry, if any
    mirror_type _mirror;
    // the process, looked up once
    string_t _pid;
    // and the host
    string_t _host;
    // the sequence number of the last record stamped
    count_type _seq;
    // the number of records that made it out
    count_type _shipped;
    // the number of records lost since the last successful write
    count_type _dropped;
    // the tail of a record the descriptor did not accept whole
    record_type _pending;
    // whether the far end has gone away
    bool _dead;

    // disallow
private:
    Courier(const Courier &) = delete;
    Courier(const Courier &&) = delete;
    const Courier & operator=(const Courier &) = delete;
    const Courier & operator=(const Courier &&) = delete;
};


// get the inline definitions
#include "Courier.icc"


// end of file
