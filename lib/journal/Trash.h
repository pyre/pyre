// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_journal_Trash_h)
#define pyre_journal_Trash_h


// a device that ignores all requests for output
class pyre::journal::Trash : public Device {
    // types
public:
    // pointers to me
    using pointer_type = std::shared_ptr<Trash>;

    using palette_type = palette_t;
    using renderer_type = renderer_t;
    using renderer_pointer = renderer_ptr;

    // metamethods
public:
    // constructor
    inline Trash();
    // destructor
    virtual ~Trash();

    // interface
public:
    // user facing messages
    virtual auto alert(const entry_type &) -> Trash & override;
    // help messages
    virtual auto help(const entry_type &) -> Trash & override;
    // developer messages
    virtual auto memo(const entry_type &) -> Trash & override;

    // data
private:
    // the renderer for alerts
    renderer_pointer _alert;
    // help messages
    renderer_pointer _help;
    // and memos
    renderer_pointer _memo;

    // disallow
private:
    Trash(const Trash &) = delete;
    Trash(const Trash &&) = delete;
    const Trash & operator=(const Trash &) = delete;
    const Trash & operator=(const Trash &&) = delete;
};


// get the inline definitions
#define pyre_journal_Trash_icc
#include "Trash.icc"
#undef pyre_journal_Trash_icc


#endif

// end of file
