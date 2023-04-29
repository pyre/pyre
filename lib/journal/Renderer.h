// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_journal_Renderer_h)
#define pyre_journal_Renderer_h


// the interface for formatting messages
class pyre::journal::Renderer {
    // types
public:
    // pointers to me
    using pointer_type = std::shared_ptr<Renderer>;

    // message content
    using entry_type = entry_t;
    using line_type = entry_type::line_type;
    using linebuf_type = entry_type::linebuf_type;
    // color table
    using palette_type = palette_t;


    // metamethods
public:
    virtual ~Renderer();
    Renderer() = default;

    // interface
public:
    virtual auto render(palette_type &, const entry_type &) const -> line_type;

    // implementation details
protected:
    virtual void header(palette_type &, linebuf_type &, const entry_type &) const;
    virtual void body(palette_type &, linebuf_type &, const entry_type &) const;
    virtual void footer(palette_type &, linebuf_type &, const entry_type &) const;

    // disallow
private:
    Renderer(const Renderer &) = delete;
    Renderer(const Renderer &&) = delete;
    const Renderer & operator= (const Renderer &) = delete;
    const Renderer & operator= (const Renderer &&) = delete;
};


#endif

// end of file
