// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external support
#include "externals.h"
// the descriptor, its flags, and the process
#include <cerrno>
#include <csignal>
#include <chrono>
#include <fcntl.h>
#include <unistd.h>
// forward declarations
#include "forward.h"
// type aliases
#include "api.h"

// message contents
#include "Entry.h"

// my superclass
#include "Device.h"
// get the courier declaration
#include "Courier.h"


// metamethods
pyre::journal::Courier::Courier(
    descriptor_type descriptor, const name_type & name, mirror_type mirror) :
    super_type(name),
    _descriptor(descriptor),
    _mirror(mirror),
    _pid(std::to_string(::getpid())),
    _host(),
    _seq(0),
    _shipped(0),
    _dropped(0),
    _pending(),
    _dead(false)
{
    // look up the host once
    char host[256] = { 0 };
    // if the lookup succeeds
    if (::gethostname(host, sizeof(host) - 1) == 0) {
        // remember it
        _host = host;
    }
    // the descriptor is never allowed to block the process that is logging
    auto flags = ::fcntl(_descriptor, F_GETFL, 0);
    // if it could be read
    if (flags != -1) {
        // switch it to non-blocking
        ::fcntl(_descriptor, F_SETFL, flags | O_NONBLOCK);
    }
    // a far end that goes away must not take this process down with a broken pipe
#ifdef F_SETNOSIGPIPE
    // where the descriptor itself can be told to report the condition rather than signal it,
    // nothing else in the process is touched
    ::fcntl(_descriptor, F_SETNOSIGPIPE, 1);
#else
    // otherwise, look at the disposition of the signal
    auto previous = ::signal(SIGPIPE, SIG_IGN);
    // if the application had expressed an opinion
    if (previous != SIG_DFL && previous != SIG_ERR) {
        // restore its choice; it is not mine to override
        ::signal(SIGPIPE, previous);
    }
#endif
    // all done
    return;
}


// destructor
pyre::journal::Courier::~Courier()
{
    // release the descriptor
    close();
    // all done
    return;
}


// interface
auto
pyre::journal::Courier::alert(const entry_type & entry) -> Courier &
{
    // deliver
    deliver(entry, "alert");
    // all done
    return *this;
}


auto
pyre::journal::Courier::help(const entry_type & entry) -> Courier &
{
    // deliver
    deliver(entry, "help");
    // all done
    return *this;
}


auto
pyre::journal::Courier::memo(const entry_type & entry) -> Courier &
{
    // deliver
    deliver(entry, "memo");
    // all done
    return *this;
}


auto
pyre::journal::Courier::close() -> Courier &
{
    // if the descriptor is still mine
    if (!_dead) {
        // release it; a descriptor that is already gone needs nothing further
        ::close(_descriptor);
        // either way, i'm done
        _dead = true;
    }
    // all done
    return *this;
}


// the pipeline
auto
pyre::journal::Courier::ship(const entry_type & entry) -> void
{
    // if the far end has gone away
    if (_dead) {
        // there is nothing to do
        return;
    }
    // finish writing whatever was left over from the last time
    if (!drain()) {
        // the far end is still not keeping up, so this entry is lost
        lose();
        // all done
        return;
    }
    // if records were lost since the last successful write
    if (_dropped) {
        // say so, on my own channel; the report takes the sequence number ahead of the entry
        // that prompted it, since it goes out first
        auto report = notice(entry);
        // if the notice could not be written
        if (!write(report)) {
            // the entry that prompted it is lost as well
            lose();
            // all done
            return;
        }
        // the drops have been reported
        _dropped = 0;
        // if the notice went out only in part
        if (!_pending.empty()) {
            // the entry must not overtake its tail, so it is lost as well
            lose();
            // all done
            return;
        }
    }
    // stamp the record
    auto record = stamp(entry);
    // write it
    if (write(record)) {
        // it is on its way
        ++_shipped;
    } else {
        // it is lost
        ++_dropped;
    }
    // all done
    return;
}


auto
pyre::journal::Courier::stamp(const entry_type & entry) -> record_type
{
    // advance the sequence
    ++_seq;
    // render the record, with the origin stamped into the notes
    return render(entry.page(), origin(entry.notes()));
}


auto
pyre::journal::Courier::notice(const entry_type & entry) -> record_type
{
    // advance the sequence
    ++_seq;
    // the page: one line with the count
    page_t page { std::to_string(_dropped) + " journal entries were dropped" };
    // the notes: my channel, the severity, and the count, so a consumer can show it without
    // parsing prose
    notes_t notes {
        { "channel", reporter },
        { "severity", "warning" },
        { "dropped", std::to_string(_dropped) },
    };
    // look for the application of the entry whose delivery prompted the report
    auto application = entry.notes().find("application");
    // if it carries one
    if (application != entry.notes().end()) {
        // copy it, so the notice stays attributable
        notes["application"] = application->second;
    }
    // render the record, with the origin stamped into the notes
    return render(page, origin(notes));
}


// implementation details
auto
pyre::journal::Courier::deliver(const entry_type & entry, const sink_type & sink) -> void
{
    // if there is a mirror
    if (_mirror) {
        // it gets the entry unchanged, through the same sink
        if (sink == "alert") {
            _mirror->alert(entry);
        } else if (sink == "memo") {
            _mirror->memo(entry);
        } else {
            _mirror->help(entry);
        }
    }
    // ship it
    ship(entry);
    // all done
    return;
}


auto
pyre::journal::Courier::lose() -> void
{
    // the entry consumes a sequence number all the same, so a consumer can tell how many
    // records it never saw by the gaps in the sequence
    ++_seq;
    // and count the loss
    ++_dropped;
    // all done
    return;
}


auto
pyre::journal::Courier::drain() -> bool
{
    // if there is nothing pending
    if (_pending.empty()) {
        // the descriptor is clear
        return true;
    }
    // take the tail
    auto data = std::move(_pending);
    // and clear it, so the write can put back whatever remains
    _pending.clear();
    // if the descriptor accepted none of it
    if (!write(data)) {
        // it is still pending, in full
        _pending = std::move(data);
        // and the descriptor is not clear
        return false;
    }
    // the descriptor is clear only if nothing remains
    return _pending.empty();
}


auto
pyre::journal::Courier::write(const record_type & data) -> bool
{
    // write as much as the descriptor will take
    auto count = ::write(_descriptor, data.data(), data.size());
    // if it will take nothing right now
    if (count < 0 && (errno == EAGAIN || errno == EWOULDBLOCK || errno == EINTR)) {
        // report the refusal
        return false;
    }
    // if the descriptor is gone
    if (count < 0) {
        // the far end went away; go quiet
        _dead = true;
        // nothing was accepted
        return false;
    }
    // if the descriptor took only part of the data
    if (static_cast<size_t>(count) < data.size()) {
        // the rest waits for the next opportunity
        _pending = data.substr(count);
    }
    // the data was accepted
    return true;
}


auto
pyre::journal::Courier::origin(const notes_t & notes) const -> notes_t
{
    // the time of the flush, in seconds since the epoch
    auto now = std::chrono::system_clock::now().time_since_epoch();
    auto seconds = std::chrono::duration_cast<std::chrono::microseconds>(now).count() / 1e6;
    // render it
    std::ostringstream stamp;
    stamp << std::fixed << std::setprecision(6) << seconds;
    // a copy of the notes
    notes_t stamped = notes;
    // with the origin on top; a note of the same name from the call site is overwritten
    stamped["pid"] = _pid;
    stamped["seq"] = std::to_string(_seq);
    stamped["time"] = stamp.str();
    stamped["host"] = _host;
    // all done
    return stamped;
}


auto
pyre::journal::Courier::render(const page_t & page, const notes_t & notes) const -> record_type
{
    // the record
    std::ostringstream record;
    // the format version, then the page
    record << "{\"journal\":1,\"page\":[";
    // a separator that is empty before the first line
    const char * separator = "";
    // go through the lines
    for (const auto & line : page) {
        // render each one
        record << separator << quote(line);
        // and separate the next
        separator = ",";
    }
    // the notes
    record << "],\"notes\":{";
    // reset the separator
    separator = "";
    // go through the notes
    for (const auto & [key, value] : notes) {
        // render each pair
        record << separator << quote(key) << ":" << quote(value);
        // and separate the next
        separator = ",";
    }
    // close the record and terminate the line
    record << "}}\n";
    // all done
    return record.str();
}


auto
pyre::journal::Courier::quote(const string_t & text) -> string_t
{
    // the literal, opened
    string_t literal = "\"";
    // go through the characters
    for (unsigned char c : text) {
        // escape what JSON requires; everything else, non-ascii included, passes through
        switch (c) {
            case '"':
                literal += "\\\"";
                break;
            case '\\':
                literal += "\\\\";
                break;
            case '\n':
                literal += "\\n";
                break;
            case '\r':
                literal += "\\r";
                break;
            case '\t':
                literal += "\\t";
                break;
            case '\b':
                literal += "\\b";
                break;
            case '\f':
                literal += "\\f";
                break;
            default:
                // the remaining control characters get the general form
                if (c < 0x20) {
                    // the hex digits
                    static const char * digits = "0123456789abcdef";
                    // render
                    literal += "\\u00";
                    literal += digits[c >> 4];
                    literal += digits[c & 0x0f];
                } else {
                    // ordinary characters pass through
                    literal += static_cast<char>(c);
                }
        }
    }
    // close the literal
    literal += "\"";
    // all done
    return literal;
}


// end of file
