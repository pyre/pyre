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

    staff = (
        bizbook.schema.Staff(person="234-88-9720", position="acquisition"),
        bizbook.schema.Staff(person="321-55-8906", position="project"),
        bizbook.schema.Staff(person="723-48-9010", position="copy"),
        bizbook.schema.Staff(person="777-02-9831", position="project"),
        bizbook.schema.Staff(person="777-66-9902", position="copy"),
        bizbook.schema.Staff(person="826-11-9034", position="project"),
        bizbook.schema.Staff(person="885-23-9140", position="project"),
        bizbook.schema.Staff(person="943-88-7920", position="acquisition"),
        bizbook.schema.Staff(person="993-86-0420", position="acquisition"),
        )
    # add them to their table
    db.insert(*staff)
    

    # make some books
    books = (
        bizbook.schema.Book(
            id="BU1032",
            title="The busy executive's database guide",
            category="business", publisher="1389", date="1985/06/12",
            description="""
            An overview of available database systems with an emphasis on business
            applications. Illustrated."
            """),
        bizbook.schema.Book(
            id="BU1111",
            title="Cooking with computers: surreptitious balance sheets",
            category="business", publisher="1389", date="1985/06/09",
            description="""
            Helpful hints on how to use your electronic resource to best advantage
            """),
        bizbook.schema.Book(
            id="BU2075",
            title="You can combat computer stress",
            category="business", publisher="0736", date="1985/06/30",
            description="""
            The latest medical and psychological techniques for living with the electronic
            office. Easy to understand explanations.
            """),

        bizbook.schema.Book(
            id="BU7832",
            title="Straight talk about computers",
            category="business", publisher="1389", date="1985/06/22",
            description="""
            Annotated analysis of what computers can do for you: a no-hype guide for the
            critical user.
            """),
        bizbook.schema.Book(
            id="MC2222",
            title="Silicon Valley gastronomic treats",
            category="modern cookbook", publisher="0877", date="1985/06/09",
            description="""
            Favorite recipes for quick, easy and elegant meals, tried and tested by people who
            never have time to eat, let alone cook.
            """),
        bizbook.schema.Book(
            id="MC3021",
            title="The gourmet microwave",
            category="modern cookbook", publisher="0877", date="1985/06/18",
            description="""
            Traditional French gourmet recipes adapted for modern microwave cooking.
            """),
        bizbook.schema.Book(
            id="MC3026",
            title="The psychology of computer cooking",
            publisher="0877"
            ),
        bizbook.schema.Book(
            id="PC1035",
            title="But is it user-friendly?",
            category="computing", publisher="1389", date="1985/06/30",
            description="""
            A survey of software for the naïve user, focusing on the 'friendliness' of each.
            """),

        bizbook.schema.Book(
            id="PC8888",
            title="Secrets of Silicon Valley",
            category="computing", publisher="1389", date="1985/06/12",
            description="""
            Muckraking reporting by two courageous women on the world's largest computer
            software and hardware manufacturers.
            """),
        bizbook.schema.Book(
            id="PC9999",
            title="Net etiquette",
            category="computing", publisher="1389",
            description="""
            A must-read for computer conference debutantes
            """),
        bizbook.schema.Book(
            id="PS1372",
            title="Computer-phobic and on-phobic individuals: behavior variations",
            category="psychology", publisher="0736", date="1985/10/21",
            description="""
            A must for the specialist, this book examines the difference between those who hate
            and fear computers and those who think they are swell.
            """),
        bizbook.schema.Book(
            id="PS2091",
            title="Is anger the enemy?",
            category="psychology", publisher="0736", date="1985/06/15",
            description="""
            Carefully researched study of the effects of strong emotions on the body. Metabolic
            charts included.
            """),
        bizbook.schema.Book(
            id="PS2106",
            title="Life without fear",
            category="psychology", publisher="0736", date="1985/10/05",
            description="""
            New exercise, meditation, and nutritional techniques that can reduce the shock of
            daily interactions. Popular audience. Sample menus included, exercise video
            available separately.
            """),

        bizbook.schema.Book(
            id="PS3333",
            title="Prolonged data deprivation: four case studies",
            category="psychology", publisher="0736", date="1985/06/12",
            description="""
            What happens when the data runs dry? Searching evaluations of information-shortage
            effects on heavy users.
            """),
        bizbook.schema.Book(
            id="PS7777",
            title="Emotional security: a new algorithm",
            category="psychology", publisher="0736", date="1985/06/12",
            description="""
            Protecting yourself and your loved ones from undue emotional stress in the modern
            world. Use of computer and nutritional aids emphasized.
            """),
        bizbook.schema.Book(
            id="TC3218",
            title="Onions, leeks and garlic: cooking secrets of the Mediterranean",
            category="cookbook", publisher="0877", date="1985/10/21",
            description="""
            Profusely illustrated in color, this makes a wonderful gift book for a
            cuisine-oriented friend.
            """),

        bizbook.schema.Book(
            id="TC7777",
            title="Sushi, Anyone?",
            category="cookbook", publisher="0877", date="1985/06/12",
            description="""
            Detailed instructions on improving your position in life by learning how to make
            authentic Japanese sushi in your spare time. 5-10% increase in number of friends
            per recipe reported from beta test.
            """),
        bizbook.schema.Book(
            id="TC4203",
            title="Fifty years in Buckingham Palace kitchens",
            category="cookbook", publisher="0877", date="1985/06/12",
            description="""
            More anecdotes from the Queen's favorite cook describing life among English
            royalty. Recipes, techniques, tender vignettes.
            """),
        )
    # add them to their table
    db.insert(*books)

    # authors
    authors = (
        bizbook.schema.Author(author="173-32-1176", book="PS3333", ordinal=1, share=1.0),
        bizbook.schema.Author(author="213-46-8915", book="BU1032", ordinal=2, share=0.4),
        bizbook.schema.Author(author="213-46-8915", book="BU2075", ordinal=1, share=1.0),
        bizbook.schema.Author(author="238-95-7766", book="PC1035", ordinal=1, share=1.0),
        bizbook.schema.Author(author="267-41-2394", book="BU1111", ordinal=2, share=0.4),
        bizbook.schema.Author(author="267-41-2394", book="TC7777", ordinal=2, share=0.3),
        bizbook.schema.Author(author="274-80-9391", book="BU7832", ordinal=1, share=1.0),
        bizbook.schema.Author(author="409-56-7008", book="BU1032", ordinal=1, share=0.6),
        bizbook.schema.Author(author="427-17-2319", book="PC8888", ordinal=1, share=0.5),
        bizbook.schema.Author(author="472-27-2349", book="TC7777", ordinal=3, share=0.3),
        bizbook.schema.Author(author="486-29-1786", book="PC9999", ordinal=1, share=1.0),
        bizbook.schema.Author(author="486-29-1786", book="PS7777", ordinal=1, share=1.0),
        bizbook.schema.Author(author="648-92-1872", book="TC4203", ordinal=1, share=1.0),
        bizbook.schema.Author(author="672-71-3249", book="TC7777", ordinal=1, share=0.4),
        bizbook.schema.Author(author="712-45-1867", book="MC2222", ordinal=1, share=1.0),
        bizbook.schema.Author(author="722-51-5454", book="MC3021", ordinal=1, share=0.75),
        bizbook.schema.Author(author="724-80-9391", book="BU1111", ordinal=1, share=0.6),
        bizbook.schema.Author(author="724-80-9391", book="PS1372", ordinal=2, share=0.25),
        bizbook.schema.Author(author="756-30-7391", book="PS1372", ordinal=1, share=0.75),
        bizbook.schema.Author(author="807-91-6654", book="TC3218", ordinal=1, share=1.0),
        bizbook.schema.Author(author="846-92-7186", book="PC8888", ordinal=2, share=0.5),
        bizbook.schema.Author(author="899-46-2035", book="MC3021", ordinal=2, share=0.25),
        bizbook.schema.Author(author="899-46-2035", book="PS2091", ordinal=2, share=0.5),
        bizbook.schema.Author(author="998-72-3567", book="PS2091", ordinal=1, share=0.5),
        bizbook.schema.Author(author="998-72-3567", book="PS2106", ordinal=1, share=1.0),
        )
    # add them to their table
    db.insert(*authors)

    editors = (
        bizbook.schema.Editor(editor="321-55-8906", book="BU1032", ordinal=2),
        bizbook.schema.Editor(editor="321-55-8906", book="BU1111", ordinal=2),
        bizbook.schema.Editor(editor="321-55-8906", book="BU2075", ordinal=3),
        bizbook.schema.Editor(editor="321-55-8906", book="BU7832", ordinal=2),
        bizbook.schema.Editor(editor="321-55-8906", book="PC1035", ordinal=2),
        bizbook.schema.Editor(editor="321-55-8906", book="PC8888", ordinal=2),
        bizbook.schema.Editor(editor="777-02-9831", book="PC1035", ordinal=3),
        bizbook.schema.Editor(editor="777-02-9831", book="PC8888", ordinal=3),
        bizbook.schema.Editor(editor="826-11-9034", book="BU2075", ordinal=2),
        bizbook.schema.Editor(editor="826-11-9034", book="PS1372", ordinal=2),
        bizbook.schema.Editor(editor="826-11-9034", book="PS2091", ordinal=2),
        bizbook.schema.Editor(editor="826-11-9034", book="PS2106", ordinal=2),
        bizbook.schema.Editor(editor="826-11-9034", book="PS3333", ordinal=2),
        bizbook.schema.Editor(editor="826-11-9034", book="PS7777", ordinal=2),
        bizbook.schema.Editor(editor="885-23-9140", book="MC2222", ordinal=2),
        bizbook.schema.Editor(editor="885-23-9140", book="MC3021", ordinal=2),
        bizbook.schema.Editor(editor="885-23-9140", book="TC3218", ordinal=2),
        bizbook.schema.Editor(editor="885-23-9140", book="TC4203", ordinal=2),
        bizbook.schema.Editor(editor="885-23-9140", book="TC7777", ordinal=2),
        bizbook.schema.Editor(editor="943-88-7920", book="BU1032", ordinal=1),
        bizbook.schema.Editor(editor="943-88-7920", book="BU1111", ordinal=1),
        bizbook.schema.Editor(editor="943-88-7920", book="BU2075", ordinal=1),
        bizbook.schema.Editor(editor="943-88-7920", book="BU7832", ordinal=1),
        bizbook.schema.Editor(editor="943-88-7920", book="PC1035", ordinal=1),
        bizbook.schema.Editor(editor="943-88-7920", book="PC8888", ordinal=1),
        bizbook.schema.Editor(editor="993-86-0420", book="MC2222", ordinal=1),
        bizbook.schema.Editor(editor="993-86-0420", book="MC3021", ordinal=1),
        bizbook.schema.Editor(editor="993-86-0420", book="PS1372", ordinal=1),
        bizbook.schema.Editor(editor="993-86-0420", book="PS2091", ordinal=1),
        bizbook.schema.Editor(editor="993-86-0420", book="PS2106", ordinal=1),
        bizbook.schema.Editor(editor="993-86-0420", book="PS3333", ordinal=1),
        bizbook.schema.Editor(editor="993-86-0420", book="PS7777", ordinal=1),
        bizbook.schema.Editor(editor="993-86-0420", book="TC3218", ordinal=1),
        bizbook.schema.Editor(editor="993-86-0420", book="TC4203", ordinal=1),
        bizbook.schema.Editor(editor="993-86-0420", book="TC7777", ordinal=1),
        )
    # add them to their table
    db.insert(*editors)
    
    # and return the component
    return db


# main
if __name__ == "__main__":
    test()


# end of file 
