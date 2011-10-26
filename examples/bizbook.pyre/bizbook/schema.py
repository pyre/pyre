# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
This file collects the table declarations for the {bizbook} database from 

    "The Practical SQL Handbook", Second Edition
    Judith S. Bowman
    Sandra L. Emerson
    Marcy Darnovsky
"""


# access the package
import pyre.db


class Location(pyre.db.table, id="locations"):
    """
    The table of addresses
    """
    id = pyre.db.str().primary()
    address = pyre.db.str()
    city = pyre.db.str()
    state = pyre.db.str()
    zip = pyre.db.str()


class Person(pyre.db.table, id="persons"):
    """
    The table of people
    """
    ssn = pyre.db.str().primary()
    lastname = pyre.db.str()
    firstname = pyre.db.str()


class Publisher(pyre.db.table, id="publishers"):
    """
    The book publishers
    """
    id = pyre.db.str().primary()
    name = pyre.db.str()
    headquarters = pyre.db.reference(key=Location.id)


class Address(pyre.db.table, id="addresses"):
    """
    The table of addresses
    """
    person = pyre.db.reference(key=Person.ssn)
    address = pyre.db.reference(key=Location.id)


class ContactMethod(pyre.db.table, id="contact_methods"):
    """
    Contact information
    """
    uid = pyre.db.str()
    method = pyre.db.str()
    person = pyre.db.reference(key=Person.ssn)


# end of file 
