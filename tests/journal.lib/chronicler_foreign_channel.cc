// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>

// type aliases
using device_t = pyre::journal::device_t;
using chronicler_t = pyre::journal::chronicler_t;
using info_t = pyre::journal::info_t;
using warning_t = pyre::journal::warning_t;


// a device that counts the entries it is handed, and says whether it is foreign
class Counter : public device_t {
    // metamethods
public:
    // a counter that is native unless told otherwise
    Counter(bool foreign = false) : device_t("counter"), entries(0), _foreign(foreign) {}
    // destructor
    ~Counter() {}

    // interface
public:
    // count user facing messages
    virtual auto alert(const entry_type &) -> Counter &
    {
        // one more
        ++entries;
        // all done
        return *this;
    }
    // count help screens
    virtual auto help(const entry_type &) -> Counter &
    {
        // one more
        ++entries;
        // all done
        return *this;
    }
    // count developer messages
    virtual auto memo(const entry_type &) -> Counter &
    {
        // one more
        ++entries;
        // all done
        return *this;
    }
    // whether i claim to be implemented outside c++
    virtual auto foreign() const -> bool
    {
        // as told
        return _foreign;
    }

    // data
public:
    // the number of entries i was handed
    int entries;

private:
    // whether i am foreign
    bool _foreign;
};


// verify that foreign devices are forgotten by channels and severities, and native ones are kept
int
main()
{
    // make a foreign device and a native one
    auto foreign = std::make_shared<Counter>(true);
    auto native = std::make_shared<Counter>();
    // give a channel the foreign device
    info_t("test.journal.foreign.channel").device(foreign);
    // and another channel the native one
    info_t("test.journal.native.channel").device(native);
    // make the foreign device the default of a severity
    warning_t::index().device(foreign);

    // detach the foreign devices
    chronicler_t::detachForeign();

    // the channel forgot its foreign device
    assert(info_t::index().lookup("test.journal.foreign.channel").device() == nullptr);
    // the other channel kept its native one
    assert(info_t::index().lookup("test.journal.native.channel").device() == native);
    // the severity forgot its default
    assert(warning_t::index().device() == nullptr);
    // and nothing in the journal holds the foreign device any more
    assert(foreign.use_count() == 1);
    // all done
    return 0;
}


// end of file
