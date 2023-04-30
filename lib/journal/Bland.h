// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_journal_Bland_h)
#define pyre_journal_Bland_h


// a formatter for messages that are meant for end user; currently, this means {info_t},
// {warning_t}, and {error_t}
class pyre::journal::Bland : public Renderer {
    // metamethods
public:
    virtual ~Bland();
    Bland() = default;

    // implementation details
protected:
    virtual void header(palette_type &, linebuf_type &, const entry_type &) const override;
    virtual void body(palette_type &, linebuf_type &, const entry_type &) const override;
    virtual void footer(palette_type &, linebuf_type &, const entry_type &) const override;

    // disallow
private:
    Bland(const Bland &) = delete;
    Bland(const Bland &&) = delete;
    const Bland & operator=(const Bland &) = delete;
    const Bland & operator=(const Bland &&) = delete;
};


#endif

// end of file
