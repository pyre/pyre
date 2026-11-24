// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// for the build system
#include <portinfo>

// the package under test
#include <pyre/postgres.h>
// the allocation this test makes fail
#include <cstdlib>
#include <new>
// so a failing test can say why
#include <iostream>


// the number of allocations to let through before one fails; set right before the allocation
// this test is about, and negative when no allocation is to fail
static auto allocationsBeforeFailure = -1;


// the allocator of the whole program, which can be told to fail once
auto
operator new(std::size_t size) -> void *
{
    // when the allocation that is to fail comes up
    if (allocationsBeforeFailure == 0) {
        // fail it, and only it
        allocationsBeforeFailure = -1;
        // the way a full heap would
        throw std::bad_alloc();
    }
    // when one is to fail later, count this one as let through
    if (allocationsBeforeFailure > 0) {
        --allocationsBeforeFailure;
    }
    // get the memory, insisting on at least a byte
    void * memory = std::malloc(size == 0 ? 1 : size);
    // and report a heap that is actually full
    if (memory == nullptr) {
        throw std::bad_alloc();
    }
    // hand it off
    return memory;
}


// and the deallocators that pair with it
auto
operator delete(void * memory) noexcept -> void
{
    // give the memory back
    std::free(memory);
    // all done
    return;
}

auto
operator delete(void * memory, std::size_t) noexcept -> void
{
    // give the memory back
    std::free(memory);
    // all done
    return;
}


// a recipe for releasing a handle that counts the releases, so the test can tell whether the
// handle it gave away was released
struct Counted {
    // types
public:
    // me
    using self_type = Counted;
    // the handles are addresses of integers
    using handle_type = int *;

    // metamethods
public:
    // the full set, so the copy and move behavior is never left to inference
    Counted() = default;
    Counted(const Counted &) = default;
    Counted(Counted &&) noexcept = default;
    Counted & operator=(const Counted &) = default;
    Counted & operator=(Counted &&) noexcept = default;
    ~Counted() = default;

    // interface
public:
    // release {handle}, and null it
    static auto free(handle_type & handle) noexcept -> void
    {
        // a handle that is already released is not counted again
        if (handle == nullptr) {
            return;
        }
        // count this one
        ++released;
        // and mark it released
        handle = nullptr;
        // all done
        return;
    }

    // data
public:
    // the number of handles released so far
    static inline auto released = 0;
};


// verify that a handle that cannot make the box it shares among its copies releases the object it
// was given, rather than lose it
int
main()
{
    // pull in the names
    using namespace pyre::postgres;

    // the object to give away
    auto object = 0;
    // make the next allocation fail
    allocationsBeforeFailure = 0;
    // attempt to
    try {
        // adopt the object; the allocation of the box is the next one
        const auto handle = Handle<Counted>(&object);
        // a handle that got its box means the allocation never failed
        std::cerr << "the handle made its box" << std::endl;
        // and the test cannot show anything
        return 1;
    }
    // the failure to allocate the box
    catch (const std::bad_alloc &) {
        // came after the object was released
        if (Counted::released != 1) {
            std::cerr << "the object was released " << Counted::released << " times" << std::endl;
            return 1;
        }
    }

    // all done
    return 0;
}


// end of file
