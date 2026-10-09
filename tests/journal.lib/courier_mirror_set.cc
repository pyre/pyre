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
using courier_t = pyre::journal::courier_t;
using entry_t = pyre::journal::entry_t;


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


// verify that the mirror of a courier can be replaced, and removed
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
    // make two mirrors
    auto first = std::make_shared<Counter>();
    auto second = std::make_shared<Counter>();
    // make a courier that mirrors to the first one
    courier_t courier(pipes[1], "courier", first);
    // make an entry
    entry_t entry;
    // send it
    courier.alert(entry);
    // the first mirror saw it
    assert(first->entries == 1);
    // switch to the second mirror
    courier.mirror(second);
    // verify the switch
    assert(courier.mirror() == second);
    // send the entry again
    courier.alert(entry);
    // only the second mirror saw it
    assert(first->entries == 1);
    assert(second->entries == 1);
    // stop the mirroring
    courier.mirror(nullptr);
    // send the entry once more
    courier.alert(entry);
    // neither mirror saw it
    assert(first->entries == 1);
    assert(second->entries == 1);
    // but all three made it to the far end
    assert(courier.shipped() == 3);
    // release the descriptor
    courier.close();
    // and the far end
    ::close(pipes[0]);
    // all done
    return 0;
}


// end of file
