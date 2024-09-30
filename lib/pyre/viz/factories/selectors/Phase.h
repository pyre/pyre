// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2024 all rights reserved

// code guard
#pragma once

// encode three color channels into a microsoft bitmap
template <class signalT, class phaseT>
class pyre::viz::factories::selectors::Phase : public pyre::flow::factory_t {
    // type aliases
public:
    // my base class
    using base_type = pyre::flow::factory_t;
    // my slots
    using signal_type = signalT;
    using phase_type = phaseT;

    // ref to me
    using factory_ref_type = std::shared_ptr<Phase>;
    // my input slots
    using signal_ref_type = std::shared_ptr<signal_type>;
    // and my output slots
    using phase_ref_type = std::shared_ptr<phase_type>;

    // factory
public:
    inline static auto create(const name_type & name = "") -> factory_ref_type;

    // metamethods
public:
    // destructor
    virtual ~Phase();
    // constructor: DON'T CALL
    inline Phase(sentinel_type, const name_type &);

    // accessors
public:
    // input slots
    auto signal() -> signal_ref_type;
    // output slots
    auto phase() -> phase_ref_type;

    // mutators
public:
    // input slots
    auto signal(signal_ref_type) -> factory_ref_type;
    // output slots
    auto phase(phase_ref_type) -> factory_ref_type;

    // flow protocol
public:
    virtual auto make(const name_type & slot, base_type::product_ref_type product)
        -> base_type::factory_ref_type override;

    // suppressed metamethods
private:
    // constructors
    Phase(const Phase &) = delete;
    Phase & operator=(const Phase &) = delete;
    Phase(Phase &&) = delete;
    Phase & operator=(Phase &&) = delete;
};

// get the inline definitions
#include "Phase.icc"

// end of file
