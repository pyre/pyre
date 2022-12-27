// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_journal_Alert_h)
#define pyre_journal_Alert_h


// a formatter for messages that are meant for end user; currently, this means {info_t},
// {warning_t}, and {error_t}
class pyre::journal::Alert : public Renderer {
    // metamethods
public:
    virtual ~Alert();
    Alert() = default;

    // implementation details
protected:
    virtual void header(palette_type &, linebuf_type &, const entry_type &) const override;
    virtual void body(palette_type &, linebuf_type &, const entry_type &) const override;
    virtual void footer(palette_type &, linebuf_type &, const entry_type &) const override;

    // configuration
private:
    const line_type _headerMarker { " >> " };
    const line_type _bodyMarker { " -- " };
    const line_type _footerMarker { " .. " };

    // disallow
private:
    Alert(const Alert &) = delete;
    Alert(const Alert &&) = delete;
    const Alert & operator=(const Alert &) = delete;
    const Alert & operator=(const Alert &&) = delete;
};


#endif

// end of file
