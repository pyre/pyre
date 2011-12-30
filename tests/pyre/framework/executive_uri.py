#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Exercise URI parsing by the executive
"""


def test():
    import pyre.framework
    executive = pyre.framework.executive()

    # the canonical case
    parts = executive.parseURI("scheme://authority/address?query#fragment")
    scheme, authority, address, query, fragment = parts
    assert scheme == 'scheme'
    assert authority == 'authority'
    assert address == '/address'
    assert query == 'query'
    assert fragment == 'fragment'

    # drop the fragment
    parts = executive.parseURI("scheme://authority/address?query")
    scheme, authority, address, query, fragment = parts
    assert scheme == 'scheme'
    assert authority == 'authority'
    assert address == '/address'
    assert query == 'query'
    assert fragment == None

    # drop the query
    parts = executive.parseURI("scheme://authority/address#fragment")
    scheme, authority, address, query, fragment = parts
    assert scheme == 'scheme'
    assert authority == 'authority'
    assert address == '/address'
    assert query == None
    assert fragment == 'fragment'

    # drop both the query and the fragment
    parts = executive.parseURI("scheme://authority/address")
    scheme, authority, address, query, fragment = parts
    assert scheme == 'scheme'
    assert authority == 'authority'
    assert address == '/address'
    assert query == None
    assert fragment == None

    # drop the fragment, the query and the authority, with an absolute address
    parts = executive.parseURI("scheme:/address")
    scheme, authority, address, query, fragment = parts
    assert scheme == 'scheme'
    assert authority == None
    assert address == '/address'
    assert query == None
    assert fragment == None

    # drop the fragment, the query and the authority, with a relative address
    parts = executive.parseURI("scheme:address")
    scheme, authority, address, query, fragment = parts
    assert scheme == 'scheme'
    assert authority == None
    assert address == 'address'
    assert query == None
    assert fragment == None

    # drop the fragment, the query and the authority, with a multi-level absolute address
    parts = executive.parseURI("scheme:/addr1/addr2")
    scheme, authority, address, query, fragment = parts
    assert scheme == 'scheme'
    assert authority == None
    assert address == '/addr1/addr2'
    assert query == None
    assert fragment == None

    # drop the fragment, the query and the authority, with a multi-level relative address
    parts = executive.parseURI("scheme:addr1/addr2")
    scheme, authority, address, query, fragment = parts
    assert scheme == 'scheme'
    assert authority == None
    assert address == 'addr1/addr2'
    assert query == None
    assert fragment == None

    # a simple case
    parts = executive.parseURI("pyre.pml")
    scheme, authority, address, query, fragment = parts
    assert scheme == None
    assert address == 'pyre.pml'
    assert query == None
    assert fragment == None

    # another simple case
    parts = executive.parseURI("/pyre/system/pyre.pml")
    scheme, authority, address, query, fragment = parts
    assert scheme == None
    assert authority == None
    assert address == '/pyre/system/pyre.pml'
    assert query == None
    assert fragment == None

    # the full set
    parts = executive.parseURI("file:///pyre.pml#anchor")
    scheme, authority, address, query, fragment = parts
    assert scheme == 'file'
    assert authority == ''
    assert address == '/pyre.pml'
    assert query == None
    assert fragment == 'anchor'

    # a poorly formed one
    try:
        executive.parseURI("&")
        assert False
    except executive.BadResourceLocatorError as error:
        assert error.reason == 'unrecognizable'

    return executive


# main
if __name__ == "__main__":
    test()


# end of file 
