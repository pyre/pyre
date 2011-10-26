#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Instantiate the postgres component
"""


def test():
    # import journal
    # journal.debug("postgres.init").active = True
    # journal.debug("postgres.execute").active = True
    # journal.debug("postgres.connection").active = True

    # access the postgres package
    import postgres

    # build a database component
    db = postgres.server(name="bizbook")
    # connect to the default database
    db.attach()


    # get the bizbook schema
    import bizbook

    # build some locations
    locations = (
        bizbook.schema.Location(
            id="p00", address="1 First Avenue", city="Boston", state="MA"),
        bizbook.schema.Location(
            id="p01", address="2 Second Avenue", city="Washington", state="DC"),
        bizbook.schema.Location(
            id="p02", address="3 Third Avenue", city="Berkeley", state="CA"),

        bizbook.schema.Location(
            id="a00", address="10932 Bigge Rd.", city="Menlo Park", state="CA", zip="94025"),
        bizbook.schema.Location(
            id="a01", address="309 63rd St.", city="Oakland", state="CA", zip="94618"),
        bizbook.schema.Location(
            id="a02", address="589 Darwin Ln.", city="Berkeley", state="CA", zip="94705"),
        bizbook.schema.Location(
            id="a03", address="22 Cleveland Av.", city="San Jose", state="CA", zip="95128"),
        bizbook.schema.Location(
            id="a04", address="5420 College Av.", city="Oakland", state="CA", zip="94609"),
        bizbook.schema.Location(
            id="a05", address="10 Mississippi Dr.", city="Lawrence", state="KS", zip="6044"),
        bizbook.schema.Location(
            id="a06", address="6223 Bateman St.", city="Berkeley", state="CA", zip="94705"),
        bizbook.schema.Location(
            id="a07", address="3410 Blonde St.", city="Palo ALto", state="CA", zip="94301"),
        bizbook.schema.Location(
            id="a08", address="PO Box 792", city="Covelo", state="CA", zip="95428"),
        bizbook.schema.Location(
            id="a09", address="18 Broadway Av.", city="San Francisco", state="CA", zip="94130"),
        bizbook.schema.Location(
            id="a10", address="22 Graybar Rd.", city="Nashville", state="TN", zip="37215"),
        bizbook.schema.Location(
            id="a11", address="55 Hillsdale Bl.", city="Corvalis", state="OR", zip="97330"),
        bizbook.schema.Location(
            id="a12", address="3 Silver Ct.", city="Walnut Creek", state="CA", zip="94595"),
        bizbook.schema.Location(
            id="a13", address="2286 Cram Pl.", city="Ann Arbor", state="MI", zip="48105"),
        bizbook.schema.Location(
            id="a14", address="3 Balding Pl.", city="Gary", state="IN", zip="46403"),
        bizbook.schema.Location(
            id="a15", address="5420 Telegraph Av.", city="Oakland", state="CA", zip="94609"),
        bizbook.schema.Location(
            id="a16", address="44 Upland Hts.", city="Oakland", state="CA", zip="94612"),
        bizbook.schema.Location(
            id="a17", address="5720 McAuley St.", city="Oakland", state="CA", zip="94609"),
        bizbook.schema.Location(
            id="a18", address="1956 Arlington Pl.", city="Rockville", state="MD", zip="20853"),
        bizbook.schema.Location(
            id="a19", address="301 Putnam", city="Vacaville", state="CA", zip="95688"),
        bizbook.schema.Location(
            id="a20", address="67 Seventh Ave.", city="Salt Lake City", state="UT", zip="84152"),

        bizbook.schema.Location(
            id="e00", address="18 Dowdy Ln.", city="Boston", state="MA", zip="02210"),
        bizbook.schema.Location(
            id="e01", address="3000 6th Str.", city="Berkeley", state="CA", zip="94710"),
        bizbook.schema.Location(
            id="e02", address="15 Sail", city="Denver", state="CO", zip="80237"),
        bizbook.schema.Location(
            id="e03", address="27 Yosemite", city="Oakland", state="CA", zip="94609"),
        bizbook.schema.Location(
            id="e04", address="1010 E. Devon", city="Chicago", state="IL", zip="60018"),
        bizbook.schema.Location(
            id="e05", address="97 Bleaker", city="Boston", state="MA", zip="02210"),
        bizbook.schema.Location(
            id="e06", address="32 Rockbill Pike", city="Rockbill", state="MD", zip="20852"),
        bizbook.schema.Location(
            id="e07", address="18 Severe Rd.", city="Berkeley", state="CA", zip="94710"),
        )
    # add them to their table
    db.insert(*locations)

    # build the publishers
    publishers = (
        bizbook.schema.Publisher(id="0736", name="New Age Books", headquarters="p00"),
        bizbook.schema.Publisher(id="0877", name="Binnet & Hardley", headquarters="p01"),
        bizbook.schema.Publisher(id="1389", name="Algodata Infosystems", headquarters="p02"),
        )
    # add them to their table
    db.insert(*publishers)

    # build the persons
    people = (
        bizbook.schema.Person(ssn="173-32-1176", lastname="White", firstname="Johnson"),
        bizbook.schema.Person(ssn="213-46-8915", lastname="Green", firstname="Marjorie"),
        bizbook.schema.Person(ssn="238-95-7766", lastname="Carson", firstname="Cheryl"),
        bizbook.schema.Person(ssn="267-41-2394", lastname="O'Leary", firstname="Michael"),
        bizbook.schema.Person(ssn="274-80-9391", lastname="Straight", firstname="Dick"),
        bizbook.schema.Person(ssn="341-22-1782", lastname="Smith", firstname="Meander"),
        bizbook.schema.Person(ssn="409-56-7008", lastname="Bennet", firstname="Abraham"),
        bizbook.schema.Person(ssn="427-17-2319", lastname="Dull", firstname="Ann"),
        bizbook.schema.Person(ssn="472-27-2349", lastname="Gringlesby", firstname="Burt"),
        bizbook.schema.Person(ssn="486-29-1786", lastname="Locksley", firstname="Chastity"),
        bizbook.schema.Person(ssn="527-72-3246", lastname="Greene", firstname="Morningstar"),
        bizbook.schema.Person(ssn="648-92-1872", lastname="Blotchet-Halls", firstname="Reginald"),
        bizbook.schema.Person(ssn="672-71-3249", lastname="Yokomoto", firstname="Akiko"),
        bizbook.schema.Person(ssn="712-45-1867", lastname="del Castillo", firstname="Innes"),
        bizbook.schema.Person(ssn="722-51-5454", lastname="DeFrance", firstname="Michel"),
        bizbook.schema.Person(ssn="724-08-9931", lastname="Stringer", firstname="Dirk"),
        bizbook.schema.Person(ssn="724-80-9391", lastname="MacFeather", firstname="Stearns"),
        bizbook.schema.Person(ssn="756-30-7391", lastname="Karsen", firstname="Livia"),
        bizbook.schema.Person(ssn="807-91-6654", lastname="Panteley", firstname="Sylvia"),
        bizbook.schema.Person(ssn="846-92-7186", lastname="Hunter", firstname="Sheryl"),
        bizbook.schema.Person(ssn="893-72-1158", lastname="McBadden", firstname="Heather"),
        bizbook.schema.Person(ssn="899-46-2035", lastname="Ringer", firstname="Anne"),
        bizbook.schema.Person(ssn="998-72-3567", lastname="Ringer", firstname="Albert"),

        bizbook.schema.Person(ssn="234-88-9720", lastname="Hunter", firstname="Amanda"),
        bizbook.schema.Person(ssn="321-55-8906", lastname="DeLongue", firstname="Martinella"),
        bizbook.schema.Person(ssn="723-48-9010", lastname="Sparks", firstname="Manfred"),
        bizbook.schema.Person(ssn="777-02-9831", lastname="Samuelson", firstname="Bernard"),
        bizbook.schema.Person(ssn="777-66-9902", lastname="Almond", firstname="Alfred"),
        bizbook.schema.Person(ssn="826-11-9034", lastname="Himmel", firstname="Eleanore"),
        bizbook.schema.Person(ssn="885-23-9140", lastname="Rutherford-Hayes", firstname="Hannah"),
        bizbook.schema.Person(ssn="943-88-7920", lastname="Kaspschek", firstname="Chistof"),
        bizbook.schema.Person(ssn="993-86-0420", lastname="McCann", firstname="Dennis"),

        )
    # add them to their table
    db.insert(*people)

    # build the addresses
    addresses = (
        bizbook.schema.Address(person="173-32-1176", address="a00"),
        bizbook.schema.Address(person="213-46-8915", address="a01"),
        bizbook.schema.Address(person="238-95-7766", address="a02"),
        bizbook.schema.Address(person="267-41-2394", address="a03"),
        bizbook.schema.Address(person="274-80-9391", address="a04"),
        bizbook.schema.Address(person="341-22-1782", address="a05"),
        bizbook.schema.Address(person="409-56-7008", address="a06"),
        bizbook.schema.Address(person="427-17-2319", address="a07"),
        bizbook.schema.Address(person="472-27-2349", address="a08"),
        bizbook.schema.Address(person="486-29-1786", address="a09"),
        bizbook.schema.Address(person="527-72-3246", address="a10"),
        bizbook.schema.Address(person="648-92-1872", address="a11"),
        bizbook.schema.Address(person="672-71-3249", address="a12"),
        bizbook.schema.Address(person="712-45-1867", address="a13"),
        bizbook.schema.Address(person="722-51-5454", address="a14"),
        bizbook.schema.Address(person="724-08-9931", address="a15"),
        bizbook.schema.Address(person="724-80-9391", address="a16"),
        bizbook.schema.Address(person="756-30-7391", address="a17"),
        bizbook.schema.Address(person="807-91-6654", address="a18"),
        bizbook.schema.Address(person="846-92-7186", address="a07"),
        bizbook.schema.Address(person="893-72-1158", address="a19"),
        bizbook.schema.Address(person="899-46-2035", address="a20"),
        bizbook.schema.Address(person="998-72-3567", address="a20"),

        bizbook.schema.Address(person="234-88-9720", address="e00"),
        bizbook.schema.Address(person="321-55-8906", address="e01"),
        bizbook.schema.Address(person="723-48-9010", address="e02"),
        bizbook.schema.Address(person="777-02-9831", address="e03"),
        bizbook.schema.Address(person="777-66-9902", address="e04"),
        bizbook.schema.Address(person="826-11-9034", address="e05"),
        bizbook.schema.Address(person="885-23-9140", address="e06"),
        bizbook.schema.Address(person="943-88-7920", address="e07"),
        bizbook.schema.Address(person="993-86-0420", address="e06"),
        )
    # add them to their table
    db.insert(*addresses)

    contacts = (
        bizbook.schema.ContactMethod(uid="408.496.7223", person="173-32-1176", method="phone"),
        bizbook.schema.ContactMethod(uid="415.986.7020", person="213-46-8915", method="phone"),
        bizbook.schema.ContactMethod(uid="415.548.7723", person="238-95-7766", method="phone"),
        bizbook.schema.ContactMethod(uid="408.286.2428", person="267-41-2394", method="phone"),
        bizbook.schema.ContactMethod(uid="415.834.2919", person="274-80-9391", method="phone"),
        bizbook.schema.ContactMethod(uid="913.843.0462", person="341-22-1782", method="phone"),
        bizbook.schema.ContactMethod(uid="415.658.9932", person="409-56-7008", method="phone"),
        bizbook.schema.ContactMethod(uid="415.836.7128", person="427-17-2319", method="phone"),
        bizbook.schema.ContactMethod(uid="707.938.6445", person="472-27-2349", method="phone"),
        bizbook.schema.ContactMethod(uid="415.585.4620", person="486-29-1786", method="phone"),
        bizbook.schema.ContactMethod(uid="615.297.2723", person="527-72-3246", method="phone"),
        bizbook.schema.ContactMethod(uid="503.745.6402", person="648-92-1872", method="phone"),
        bizbook.schema.ContactMethod(uid="415.935.4228", person="672-71-3249", method="phone"),
        bizbook.schema.ContactMethod(uid="615.996.8275", person="712-45-1867", method="phone"),
        bizbook.schema.ContactMethod(uid="219.547.9982", person="722-51-5454", method="phone"),
        bizbook.schema.ContactMethod(uid="415.843.2991", person="724-08-9931", method="phone"),
        bizbook.schema.ContactMethod(uid="415.354.7128", person="724-80-9391", method="phone"),
        bizbook.schema.ContactMethod(uid="415.534.9219", person="756-30-7391", method="phone"),
        bizbook.schema.ContactMethod(uid="301.946.8853", person="807-91-6654", method="phone"),
        bizbook.schema.ContactMethod(uid="415.836.7128", person="846-92-7186", method="phone"),
        bizbook.schema.ContactMethod(uid="707.448.4982", person="893-72-1158", method="phone"),
        bizbook.schema.ContactMethod(uid="801.826.0752", person="899-46-2035", method="phone"),
        bizbook.schema.ContactMethod(uid="801.862.0752", person="998-72-3567", method="phone"),

        bizbook.schema.ContactMethod(uid="617.432.5586", person="234-88-9720", method="phone"),
        bizbook.schema.ContactMethod(uid="415.843.2222", person="321-55-8906", method="phone"),
        bizbook.schema.ContactMethod(uid="303.721.3388", person="723-48-9010", method="phone"),
        bizbook.schema.ContactMethod(uid="415.843.6990", person="777-02-9831", method="phone"),
        bizbook.schema.ContactMethod(uid="312.699.4177", person="777-66-9902", method="phone"),
        bizbook.schema.ContactMethod(uid="617.423.0552", person="826-11-9034", method="phone"),
        bizbook.schema.ContactMethod(uid="301.468.3909", person="885-23-9140", method="phone"),
        bizbook.schema.ContactMethod(uid="415.549.3909", person="943-88-7920", method="phone"),
        bizbook.schema.ContactMethod(uid="301.468.3909", person="993-86-0420", method="phone"),
        )
    # add them to their table
    db.insert(*contacts)

    # and return the component
    return db


# main
if __name__ == "__main__":
    test()


# end of file 
