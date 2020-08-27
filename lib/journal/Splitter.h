// -*- c++ -*-
//
// the pyre authors
// (c) 1998-2020 all rights reserved

#if !defined(pyre_journal_Splitter_h)
#define pyre_journal_Splitter_h

// a middleman plumbing device that splits one input to any number of outputs
class pyre::journal::Splitter : public Device
{
protected:
    using output_t = std::shared_ptr<Device>;
    using outputs_t = std::vector<output_t>;

private:
    outputs_t _outputs;

public:
    // constructors
    Splitter();
    Splitter(std::vector<output_t> o);

    // destructor
    virtual ~Splitter() = default;

    // accessors
    auto & outputs() { return _outputs; }
    void attach(output_t output);

    virtual auto memo(const entry_type & entry) -> Splitter & override;
    virtual auto alert(const entry_type & entry) -> Splitter & override;
};

#endif

// end of file
