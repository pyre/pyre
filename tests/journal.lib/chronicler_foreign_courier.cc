// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>
#include <unistd.h>

// type aliases
using device_t = pyre::journal::device_t;
using chronicler_t = pyre::journal::chronicler_t;
using courier_t = pyre::journal::courier_t;
using splitter_t = pyre::journal::splitter_t;
using info_t = pyre::journal::info_t;


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


// verify that a foreign mirror is detached from a courier, and the mirrors of native ones are
// walked
int
main()
{
    // make a pipe
    int pipes[2];
    // the call must happen whether or not assertions are compiled in, so check it by hand
    if (::pipe(pipes) != 0) {
        // no pipe, no test
        return 1;
    }
    // make a foreign device and a native one
    auto foreign = std::make_shared<Counter>(true);
    auto native = std::make_shared<Counter>();
    // make a courier that mirrors to the foreign device
    auto direct = std::make_shared<courier_t>(pipes[1], "direct", foreign);
    // make a splitter over the foreign device and the native one
    auto splitter = std::make_shared<splitter_t>();
    // attach them
    splitter->attach(foreign).attach(native);
    // make a courier that mirrors to the splitter, writing to a descriptor of its own
    auto indirect = std::make_shared<courier_t>(::dup(pipes[1]), "indirect", splitter);
    // give one channel the first courier
    info_t("test.journal.foreign.direct").device(direct);
    // and another the second one
    info_t("test.journal.foreign.indirect").device(indirect);

    // detach the foreign devices
    chronicler_t::detachForeign();

    // the first courier stays, without its mirror
    assert(info_t::index().lookup("test.journal.foreign.direct").device() == direct);
    assert(direct->mirror() == nullptr);
    // the second one keeps its native mirror
    assert(indirect->mirror() == splitter);
    // which holds only the native device
    assert(splitter->outputs().size() == 1);
    assert(splitter->outputs()[0] == native);
    // and nothing in the journal holds the foreign device any more
    assert(foreign.use_count() == 1);

    // release the descriptors
    direct->close();
    indirect->close();
    // and the far end
    ::close(pipes[0]);
    // all done
    return 0;
}


// end of file
